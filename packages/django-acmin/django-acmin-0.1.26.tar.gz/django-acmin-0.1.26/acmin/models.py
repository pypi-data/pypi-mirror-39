from django.urls import reverse

from .utils import import_class


class ModelMixin:
    creatable = True
    editable = True
    removable = True
    cloneable = True
    exportable = True
    viewable = True
    operable = True
    selectable = False
    show_index = False
    search_fields = None
    list_exclude = None
    list_fields = None
    form_exclude = None
    form_fields = None

    def get_absolute_url(self):
        return reverse(self.__class__.__name__ + "-update", kwargs={"pk": self.pk})

    @property
    def color(self):
        return "black"


def import_model(app_name, name):
    from django.apps import apps as django_apps
    if isinstance(name, str):
        result = None
        if "." in name:  # "hotel.Channel"
            result = django_apps.get_model(name)
        if not result:
            try:
                result = django_apps.get_model(app_name, name.lower())
            except Exception:
                pass
        if not result:
            try:
                result = import_class("%s.models.%s" % (app_name, name.capitalize()))
            except Exception:
                pass

        if result:
            return result
        raise Exception(f"Cannot import model by {app_name} {name}")
