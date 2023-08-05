import logging

from acmin.forms import load_form
from acmin.utils import attrs, memorize, import_class

logger = logging.getLogger(__name__)


@memorize
def get_base_view_class(app_name, action):
    return import_class(f"{app_name}.views.Base{action.capitalize()}View")


def get_view(app_name, name, action):
    view_name = "%s%sView" % (name, action.capitalize())
    view = None
    try:
        view = import_class('%s.views.%s' % (app_name, view_name))
    except Exception:
        try:
            model_name = "%s.models.%s" % (app_name, name)
            entity = import_class(model_name)
            view = type("Dynamic%s" % view_name, (get_base_view_class(app_name, action),), dict(
                model=entity,
                __module__=f'{app_name}.{__name__}',

            ))
        except Exception as e:
            logger.error(e)

    if view and attrs.attr(view, 'form_class', None) is None:
        setattr(view, "form_class", load_form(app_name, view.model))

    return view.as_view()
