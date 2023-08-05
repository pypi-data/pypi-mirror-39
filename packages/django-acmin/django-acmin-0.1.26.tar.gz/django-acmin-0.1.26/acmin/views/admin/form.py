from collections import OrderedDict

from django.contrib.messages.views import SuccessMessageMixin
from django.forms import ChoiceField

from acmin.utils import attr, get_ancestor_attribute, get_ancestors, get_ancestors_names
from .mixins import StaticFilterMixin,ContextMixin,AccessMixin


class AdminFormView(SuccessMessageMixin, StaticFilterMixin,ContextMixin,AccessMixin):
    def get_template_names(self):
        return [f"admin/{self.model.__name__}/form.html", 'base/form.html']

    def get_removed_fields(self):
        return []

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        self._add_relation_choices(context)
        context["ancestors"] = self.get_ancestor_attribute_variables()
        context["model"] = self.model
        context["model_name"] = self.model.__name__

        return context

    def get_ancestor_attribute_variables(self):
        cls = self.model
        ancestors = list(reversed(get_ancestors(cls, self.get_max_cls())))
        length = len(ancestors)
        filters = self.get_static_filter()

        def to_dict(chain):
            name, cls = chain
            return dict(
                name=name,
                class_name=cls.__name__,
                filters={k: v for (c, d) in filters if c is cls for k, v in d.items()}
            )

        result = [dict(
            name=name,
            child=to_dict(ancestors[index + 1]),
            offsprings=[to_dict(c) for c in ancestors[index + 1:length]]
        ) for index, (name, cls) in enumerate(ancestors[0:length - 1])]
        return result

    def _add_relation_choices(self, context):
        obj = attr(context, "object")
        form = context["form"]
        choices = []
        max_cls = self.get_max_cls()
        chain_names = get_ancestors_names(self.model, max_cls)
        length = len(chain_names)
        chains = get_ancestors(self.model, max_cls)
        removed_fields = self.get_removed_fields()
        for index, (attribute, cls) in enumerate(chains):
            if attribute not in removed_fields:
                # print(attribute)
                queryset = cls.objects
                filters = self.get_static_filter()
                f = {k: v for c, f in filters if c is cls for k, v in f.items()}
                if f:
                    queryset = queryset.filter(**f)

                obj = attr(obj, attribute)
                if obj and index < length - 1:
                    parent_attribute_name = chain_names[index + 1]
                    parent_id = attr(obj, parent_attribute_name + ".id")
                    if parent_id:
                        f = {parent_attribute_name + "_id": parent_id}
                        queryset = queryset.filter(**f)
                else:
                    for c, f in filters:
                        relation = get_ancestor_attribute(cls, c)
                        if relation:
                            f = {relation.replace(".", "__") + "__" + key: value for key, value in f.items()}
                            queryset = queryset.filter(**f)

                choices.append((attribute, ChoiceField(
                    required=True if form.fields.pop(attribute, False) else False,
                    initial=attr(obj, "id"),
                    label=attr(cls, '_meta.verbose_name'),
                    choices=[('', '-----')] + [(e.id, str(e)) for e in queryset.all()]
                )))
        choices.reverse()

        fields = OrderedDict(choices)
        fields.update(form.fields)
        for f in removed_fields:
            fields.pop(f, None)
        form.fields = fields
