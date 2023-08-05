import collections

from django.db.models.fields.related import ForeignKey, OneToOneField

from . import attr, auto_repr, first, memorize


class Relation(object):
    def __init__(self, model, attribute, verbose_name):
        self.model = model
        self.attribute = attribute
        self.verbose_name = verbose_name

    def __repr__(self):
        return ""f"{self.model},{self.attribute},{self.verbose_name}"""


class MultipleRelation(object):
    def __init__(self, model, attributes, verbose_names):
        self.model = model
        self.attributes = attributes
        self.verbose_names = verbose_names

    def __repr__(self):
        return f"{self.model},{self.attributes},{self.verbose_names}"


def get_relation1(model):
    relations = []
    fields = attr(model, '_meta.fields')
    for field in fields:
        remote_field = attr(field, "remote_field")
        if remote_field:
            related_model = attr(remote_field, "model")
            field = attr(remote_field, "field")
            if type(field) in (ForeignKey, OneToOneField):
                relations.append((related_model, attr(field, "name")))
    return relations


def _get_attributes(model, name=None):
    relations = get_relation1(model)
    names = []
    for relation_model, relation_attribute in relations:
        new_name = f"{name}.{relation_attribute}" if name else relation_attribute
        new_names = _get_attributes(relation_model, new_name)
        if new_names:
            names += new_names
        else:
            names.append(new_name)

    return names


def get_multiple_relation_group(model):
    class_relations = collections.defaultdict(list)
    group = get_relation_group(model)
    for relations in group:
        for relation in relations:
            class_relations[relation.model].append(relation)

    result = []
    for relations in group:
        new_relations = []
        for relation in relations:
            all_relation = class_relations.pop(relation.model, None)
            if all_relation:
                attributes = [r.attribute for r in all_relation]
                verbose_names = [r.verbose_name for r in all_relation]
                new_relations.append(MultipleRelation(
                    relation.model, attributes, verbose_names))
        if new_relations:
            result.append(new_relations)

    for relations in group:
        print(relations)
    print("----------------------------")
    for relations in result:
        print(relations)

    return result


@memorize
def get_relation_group(model):
    group, relations = [], []
    last_attribute = None
    for attribute in _get_attributes(model):
        names = attribute.split(".")
        for i in range(1, len(names) + 1):
            sub_attribute, cls, verbose_name = ".".join(
                names[0:i]), model, None
            for name in sub_attribute.split("."):
                field = attr(cls, f"{name}.field")
                verbose_name = attr(field, "_verbose_name")
                cls = attr(field, f"remote_field.model")
            if not verbose_name:
                verbose_name = attr(cls, "_meta.verbose_name")
            # print(verbose_name)
            relation = Relation(cls, sub_attribute, verbose_name)
            if not relations or sub_attribute.startswith(last_attribute):
                relations.append(relation)
            elif relations:
                group.append(relations)
                relations = [relation]
            last_attribute = sub_attribute

    if relations:
        group.append(relations)

    return group


@memorize
def get_model_fields(cls) -> list:
    return attr(cls, '_meta.fields')


@memorize
def get_model_fields_without_relation(model):
    fields = model._meta.fields
    result = []
    for field in fields:
        name = field.name
        if 'ForeignKey' in str(field.__class__):
            name = "%s|%s_id" % (name, name)
        result.append(name)
    return result


@memorize
def get_many_to_many_fields(cls) -> list:
    return attr(cls, '_meta.many_to_many')


def get_model_field(cls, name):
    return first([f for f in attr(cls, '_meta.fields') if f.name == name])


@memorize
def get_model_field_names(cls) -> list:
    return [x.name for x in get_model_fields(cls)]


@memorize
def get_ancestor_attribute(child_cls, parent_cls, property_name=""):
    for name, x in get_parents(child_cls):
        name = name if not property_name else property_name + "." + name
        if x is child_cls or x is parent_cls:
            return name

        return get_ancestor_attribute(x, parent_cls, name)


@memorize
def get_ancestors(cls, max_cls=None):
    result = []
    if max_cls and not get_ancestor_attribute(cls, max_cls):
        return result
    if cls is not max_cls:
        foreign_fields = get_parents(cls)
        if foreign_fields:
            name, foreign_cls = foreign_fields[0]

            result.append((name, foreign_cls))
            if foreign_cls is not max_cls and foreign_cls is not cls:
                result += get_ancestors(foreign_cls, max_cls)
    return result


@memorize
def get_ancestors_names(cls, max_cls=None):
    return [name for (name, _) in get_ancestors(cls, max_cls)]


@memorize
def get_parents(cls) -> list:
    result = []
    for field in get_model_fields(cls):
        related_fields = attr(field, '_related_fields')
        if related_fields and isinstance(related_fields, list):
            item = related_fields[0]
            if isinstance(item, tuple):
                (i, _) = item
                if isinstance(i, ForeignKey):
                    result.append((field.name, i.related_model))
    return result


@auto_repr
class Field:
    def __init__(self, name, verbose, attribute_name, class_name=None, orderable=True, is_image=False):
        self.name = name
        self.verbose = verbose
        self.attribute_name = attribute_name
        self.class_name = class_name
        self.orderable = orderable
        self.is_image = is_image

# @memorize
