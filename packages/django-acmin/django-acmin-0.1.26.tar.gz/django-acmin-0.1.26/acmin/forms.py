from django import forms

from acmin.models import import_model
from acmin.utils import attrs, import_class, memorize


def get_dynamic_form(app_name, model, form_exclude=None):
    form_exclude = form_exclude or []
    if isinstance(model, str):
        model = import_model(app_name, model)

    '''
    class BaseForm(forms.ModelForm):
      class Meta:
        model=form_model
        fields=attrs.attr(model,"form_fields","__all__")
        exclude=attrs.attr(model,"form_exclude",[])

    return BaseForm
    '''
    return type("Dynamic%sForm" % model.__name__, (forms.ModelForm,), dict(
        Meta=type("Meta", (), dict(
            model=model,
            fields=attrs.attr(model, "form_fields", "__all__"),
            exclude=attrs.attr(model, "form_exclude", []) + form_exclude
        )),
        __module__=__name__
    ))


@memorize
def load_form(app_name, model):
    try:
        form = import_class("%s.forms.%sForm" % (app_name, model.__name__))
    except Exception:
        form = get_dynamic_form(app_name, model)
    return form
