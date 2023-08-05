import operator
from collections import OrderedDict
from functools import reduce

from django.db.models import Q
from django.forms import ChoiceField, forms
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.views import generic
from django.views.generic.list import BaseListView

from acmin.utils import (
    attr, first, get_ancestor_attribute, get_ancestors, get_ancestors_names, get_model_field_names
)
from acmin.utils import models as model_util
from .mixins import StaticFilterMixin, ContextMixin, AccessMixin


class SearchMixin(BaseListView):
    def get_toolbar_search_params(self):
        groups = model_util.get_relation_group(self.model)
        if groups:
            relation_names = [x.attribute for x in reduce(operator.add, groups)]
            return {k: v for k, v in self.request.GET.items() if k in relation_names and v}
        return {}

    def get_request_model_filters(self):
        return {k: v for k, v in self.request.GET.items() if k in get_model_field_names(self.model) and v}


class FuzzySearchMixin(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get("sk")
        if keyword and len(keyword) > 0:
            search_fields = attr(self.model, "search_fields")
            if search_fields:
                q = Q()
                for field in search_fields:
                    q = q | Q(**{'%s__icontains' % field: keyword})
                queryset = queryset.filter(q)

        return queryset


class FilterForm(forms.Form):
    pass


class ToolbarSearchFormMixin(SearchMixin, StaticFilterMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["toolbar_search_form"] = self.get_toolbar_search_form()
        names = [x for x in get_ancestors_names(self.model, self.get_max_cls())]
        context['hierarchy'] = {e: names[0:index] for index, e in enumerate(names)}
        return context

    def get_toolbar_search_form(self):
        choices = self.get_toolbar_search_fields()
        # print(choices)
        choices += self.get_toolbar_extra_search_choices()
        if choices:
            fields = OrderedDict(choices)
            form = FilterForm()
            form.fields = fields
            return form

    def get_toolbar_extra_search_choices(self):
        return []

    def _get_queryset_from_static_filters(self, cls):
        queryset = cls.objects
        filters = self.get_static_filter()
        if filters:
            for ancestor_cls, ancestor_filters in filters:
                attribute = get_ancestor_attribute(cls, ancestor_cls)
                if attribute:
                    f = {attribute.replace(".", "__") + "_" + key: value for key, value in ancestor_filters.items()}
                    queryset = cls.objects.filter(**f)
        return queryset

    def get_toolbar_search_fields(self):
        choices = []

        relation_groups = model_util.get_relation_group(self.model)
        params = self.get_toolbar_search_params()

        for relations in relation_groups:
            last_cls, last_name = None, None
            relations = list(reversed(relations))
            for relation in relations:
                name = relation.attribute
                cls = relation.model
                #print(name,cls)
                queryset = None
                if last_name:
                    value = params.get(last_name, None)
                    if value:
                        attribute = get_ancestor_attribute(cls, last_cls)
                        queryset = cls.objects.filter(**{attribute.replace(".", "__") + "_id": value})
                else:
                    queryset = self._get_queryset_from_static_filters(cls)

                if queryset:
                    static_filter = {}
                    for (c, f) in self.get_static_filter():
                        if c is cls:
                            static_filter.update(f)
                    if static_filter:
                        queryset = queryset.filter(**static_filter)

                options = [(e.id, str(e)) for e in queryset.all()] if queryset else []
                if options:
                    label = attr(cls, '_meta.verbose_name')
                    choices.append((name, ChoiceField(
                        initial=params.get(name, ""),
                        label=label,
                        choices=[('', '选择%s' % label)] + options,
                    )))
                    last_cls, last_name = cls, name

        return choices


class OrderMixin(BaseListView):
    def get_queryset(self):
        queryset = super().get_queryset()
        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort.replace('.', '__'))

        return queryset


class ToolbarSearchMixin(SearchMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        params = self.get_toolbar_search_params()
        for relations in model_util.get_relation_group(self.model):
            for relation in relations:
                value = params.get(relation.attribute, None)
                if value:
                    queryset = queryset.filter(**{relation.attribute.replace(".", "__") + "_id": value})
                    break

        model_filters = self.get_request_model_filters()
        if model_filters:
            queryset = queryset.filter(**model_filters)

        sort = self.request.GET.get("sort")
        if sort:
            queryset = queryset.order_by(sort.replace('.', '__'))

        return queryset


class JsonResponseMixin(BaseListView):
    def get(self, request, *args, **kwargs):
        if self.request.GET.get("format") == 'json':
            entities = [model_to_dict(item) for item in self.get_queryset()]
            return JsonResponse(entities, safe=False)

        return super().get(request, args, kwargs)


class AdminStaticListFilterMixin(StaticFilterMixin):
    def get_queryset(self):
        queryset = super().get_queryset()
        chains = get_ancestors(self.model)
        for cls, filters in self.get_static_filter():
            if self.model is cls:
                queryset = queryset.filter(**filters)
            else:
                index = first([index for index, (_, c) in enumerate(chains) if c is cls])
                if index is not None:
                    attribute = ".".join([name for name, _ in chains[0:index + 1]])
                    new_filters = {attribute.replace(".", "__") + "__" + k: v for k, v in filters.items()}
                    # print(new_filters)
                    queryset = queryset.filter(**new_filters)

        return queryset


class AdminListView(
    JsonResponseMixin,
    AdminStaticListFilterMixin,
    FuzzySearchMixin,
    ToolbarSearchFormMixin,
    ToolbarSearchMixin,
    OrderMixin,
    ContextMixin,
    AccessMixin,
    generic.ListView
):
    context_object_name = 'list'
    paginate_by = 30
    form_class = None

    def get_toolbar_search_fields(self):
        return super().get_toolbar_search_fields()

    def get_model_exclude_names(self):
        return attr(self.model, "list_exclude", [])

    def get_model_include_names(self):
        return attr(self.model, "list_fields")

    def get_model_list_fields(self):
        cls = self.model
        names = self.get_model_include_names()
        model_fields = model_util.get_model_fields(cls)
        field_dict = OrderedDict([(f.name, f) for f in model_fields])
        if names == '__all__' or not names:
            names = [f.name for f in model_fields]
        excludes = self.get_model_exclude_names()
        excludes = excludes + ['id', 'created', 'modified'] + [
            f.name for f in model_fields if f.related_model
        ]
        result = []
        for name in names:
            verbose_name = None
            orderable = True
            if isinstance(name, tuple):
                name, verbose_name = name
                orderable = False
            if name not in excludes:
                if not verbose_name:
                    verbose_name = field_dict[name].verbose_name if name in field_dict else name
                field = model_util.Field(name, verbose_name, name, None, orderable)
                result.append(field)

        return result

    def get_relation_fields(self):
        from acmin.utils import models
        fields = [model_util.Field(relation.attribute.split(".").pop(), relation.verbose_name, relation.attribute, relation.model.__name__)
                  for relations in models.get_relation_group(self.model) for relation in relations]

        fields.reverse()
        return fields

    def get_list_fields(self):
        return self.get_relation_fields() + self.get_model_list_fields()

    def get_template_names(self):
        return [f'admin/{self.model.__name__}/list.html', 'base/list.html']

    def get_context_data(self, **kwargs):
        from django.conf import settings
        context = super().get_context_data(**kwargs)
        context["view_type"] = 'list'
        context["media_url"] = attr(settings, "MEDIA_URL", "aaaa")
        context["image_height"] = getattr(settings, "ACMIN_IMAGE_HEIGHT", 80)
        context.update({"list_fields": self.get_list_fields(), })
        return context
