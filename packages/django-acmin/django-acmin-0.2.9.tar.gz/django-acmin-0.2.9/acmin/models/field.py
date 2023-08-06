from collections import defaultdict

import django.apps
from django.db import models
from django.db.models import ForeignKey
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from filelock import FileLock

from acmin.utils import first, attr
from .base import AcminModel
from .contenttype import ContentType
from .group import Group
from .user import User

cache = defaultdict(lambda: defaultdict(list))

lock = FileLock("field.lock")
lock.release(force=True)


@receiver(post_save)
@receiver(post_delete)
def handle_model_change(sender, **kwargs):
    if sender in [Group, User, Field, UserField, GroupField]:
        with lock:
            cache.clear()


def get_all_fields():
    if not cache:
        with lock:
            temp_cache = defaultdict(lambda: defaultdict(dict))
            for field in Field.objects.all():
                model = field.base.get_model()
                for user in User.objects.all():
                    temp_cache[user][model][field.attribute] = field

            base_attributes = ['sequence', 'listable', 'formable', 'sortable', 'exportable', 'verbose_name']
            for group_field in GroupField.objects.all():
                field = group_field.field
                model = field.base.get_model()
                for user in User.objects.filter(group=group_field.group).all():
                    default_field = temp_cache[user][model][field.attribute]
                    for attribute in base_attributes:
                        setattr(default_field, attribute, getattr(group_field, attribute))

            for user_field in UserField.objects.all():
                field = user_field.field
                model = field.base.get_model()
                default_field = temp_cache[user][model][field.attribute]
                for attribute in base_attributes:
                    setattr(default_field, attribute, getattr(user_field, attribute))

            for user, model_map in temp_cache.items():
                for model, field_dict in model_map.items():
                    cache[user][model] = sorted(field_dict.values(), key=lambda f: (f.group_sequence, f.sequence))

    return cache


class BaseField(AcminModel):
    class Meta:
        abstract = True

    sequence = models.IntegerField("序号")
    listable = models.BooleanField("在列表中显示", default=True)
    formable = models.BooleanField("在表单中显示", default=True)
    sortable = models.BooleanField("可排序", default=True)
    exportable = models.BooleanField("可导出", default=True)
    nullable = models.BooleanField("可以为空", default=False)
    unique = models.BooleanField("是否唯一性", default=False)
    default = models.CharField("默认值", max_length=500, null=True, blank=True)
    editable = models.BooleanField("可编辑", default=True)
    verbose_name = models.CharField("显示名称", max_length=200)


class Field(BaseField):
    class Meta:
        ordering = ['base', 'group_sequence', 'sequence']
        verbose_name_plural = verbose_name = "字段"
        # unique_together = (("base", "attribute"))

    base = models.ForeignKey(ContentType, on_delete=models.CASCADE, verbose_name="模型", related_name="base")
    attribute = models.CharField("字段名称", max_length=100)
    contenttype = models.ForeignKey(ContentType, verbose_name="字段模型", null=True, blank=True, on_delete=models.CASCADE, related_name="contenttype")
    group_sequence = models.IntegerField("分组序号")
    python_type = models.CharField("原生类型", max_length=200)

    def __str__(self):
        return f"{self.base},{self.verbose_name}({self.attribute})"

    @classmethod
    def get_field(cls, user, model, attribute):
        return first([field for field in get_all_fields()[user][model] if field.attribute == attribute])

    @classmethod
    def get_fields(cls, user, model, has_contenttype=None):
        result = []
        for field in get_all_fields()[user][model]:
            if has_contenttype is None or (has_contenttype is True and field.contenttype) or (has_contenttype is False and not field.contenttype):
                result.append(field)
        return result

    @property
    def model(self):
        if self.contenttype:
            return self.contenttype.get_model()

    @property
    def class_name(self):
        return attr(self.model, "__name__")

    @classmethod
    def get_group_fields(cls, user, model, has_contenttype=None, reverse=False):
        result = []
        group_sequence = -1
        fields = []
        for field in cls.get_fields(user, model, has_contenttype):
            if group_sequence != field.group_sequence:
                group_sequence = field.group_sequence
                if fields:
                    result.append(fields)
                fields = []
            fields.append(field)
        if fields:
            result.append(fields)

        for i in range(len(result)):
            fields = sorted(result[i], key=lambda f: (f.group_sequence, f.sequence))
            result[i] = list(reversed(fields)) if reverse else fields

        return result


class GroupField(BaseField):
    class Meta:
        ordering = ["group", 'field']
        verbose_name_plural = verbose_name = "字段(用户组)"
        unique_together = [("group", "field")]

    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE, verbose_name="默认字段")

    def __str__(self):
        return f"{self.group},{self.verbose_name}({self.field.attribute})"


class UserField(BaseField):
    class Meta:
        ordering = ["user", 'field']
        verbose_name_plural = verbose_name = "字段(用户)"
        unique_together = [("user", "field")]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user},{self.verbose_name}({self.field.attribute})"


def get_attributes(cls, name=None):
    result = []
    foreign_fields = [(attr(f, "remote_field.model"), attr(f, "remote_field.field.name")) for f in attr(cls, '_meta.fields') if issubclass(type(attr(f, "remote_field.field")), ForeignKey)]
    for foreign_model, foreign_attribute in foreign_fields:
        new_name = f"{name}.{foreign_attribute}" if name else foreign_attribute
        new_names = get_attributes(foreign_model, new_name)
        if new_names:
            result += new_names
        else:
            result.append(new_name)

    return result


def init_fields(type_map):
    new = []
    for model in django.apps.apps.get_models():
        if issubclass(model, AcminModel):
            group_sequence = 100
            base = type_map.get(model)
            attributes = []
            exists = set(f.attribute for f in Field.objects.filter(base=base).all())
            fields = [field for field in attr(model, '_meta.fields') if not attr(field, "remote_field")]
            for sequence, field in enumerate(fields, start=1):
                attribute, verbose_name = attr(field, "name"), attr(field, '_verbose_name')
                attributes.append(attribute)
                field_type = type(field)
                python_type = f"{field_type.__module__}.{field_type.__name__}"
                attributes.append(attribute)
                if attribute not in exists:
                    editable = formable = attr(field, "editable") and attribute != "id"
                    new.append(Field(
                        base=base,
                        group_sequence=group_sequence,
                        sequence=sequence,
                        attribute=attribute,
                        verbose_name=verbose_name,
                        nullable=attr(field, "null"),
                        editable=editable,
                        formable=formable,
                        python_type=python_type,
                    ))

            last_attribute, group_sequence = None, 0
            for attribute in get_attributes(model):
                names = attribute.split(".")
                for sequence in range(1, len(names) + 1):
                    sub_attribute, cls, verbose_name, field = ".".join(names[0:sequence]), model, None, None
                    if last_attribute and not sub_attribute.startswith(last_attribute):
                        group_sequence += 1
                    for name in sub_attribute.split("."):
                        field = attr(cls, f"{name}.field")
                        verbose_name = attr(field, "_verbose_name")
                        cls = attr(field, f"remote_field.model")

                    if sub_attribute not in exists:
                        editable = formable = attr(field, "editable")
                        new.append(Field(
                            base=base,
                            group_sequence=group_sequence,
                            sequence=sequence - 1,
                            attribute=sub_attribute,
                            contenttype=type_map[cls],
                            verbose_name=verbose_name or attr(cls, "_meta.verbose_name"),
                            nullable=attr(field, "null"),
                            editable=editable,
                            formable=formable,
                            python_type=ForeignKey.__module__ + "." + ForeignKey.__name__
                        ))

                    attributes.append(sub_attribute)
                    last_attribute = sub_attribute

            Field.objects.filter(base=base).exclude(attribute__in=attributes).delete()
    Field.objects.bulk_create(new)
