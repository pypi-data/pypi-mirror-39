from acmin.utils import attr


class AccessMixin:
    from django.contrib.auth import REDIRECT_FIELD_NAME
    login_url = None
    permission_denied_message = ''
    raise_exception = False
    redirect_field_name = REDIRECT_FIELD_NAME

    def get_login_url(self):
        from django.core.exceptions import ImproperlyConfigured
        from django.conf import settings
        login_url = self.login_url or settings.LOGIN_URL
        if not login_url:
            raise ImproperlyConfigured(
                '{0} is missing the login_url attribute. Define {0}.login_url, settings.LOGIN_URL, or override '
                '{0}.get_login_url().'.format(self.__class__.__name__)
            )
        return str(login_url)

    def get_permission_denied_message(self):
        return self.permission_denied_message

    def get_redirect_field_name(self):
        return self.redirect_field_name

    def handle_no_permission(self):
        from django.contrib.auth.views import redirect_to_login
        from django.core.exceptions import PermissionDenied
        if self.raise_exception or self.request.user.is_authenticated:
            raise PermissionDenied(self.get_permission_denied_message())
        return redirect_to_login(self.request.get_full_path(), self.get_login_url(), self.get_redirect_field_name())

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.has_permisson():
            return super().dispatch(request, *args, **kwargs)
        else:
            return self.handle_no_permission()

    def has_permisson(self):
        return True


class StaticFilterMixin:
    def get_max_cls(self):
        return None

    def get_static_filter(self):
        return []


class ContextMixin(object):
    @property
    def user(self):
        return attr(self, "request.user")

    def is_creatable(self) -> bool:
        return self.model.creatable

    def is_cloneable(self) -> bool:
        return self.model.cloneable

    def is_exportable(self) -> bool:
        return self.model.exportable

    def is_editable(self) -> bool:
        return self.model.editable

    def is_removable(self) -> bool:
        return self.model.removable

    def is_viewable(self) -> bool:
        return self.model.viewable

    def is_operable(self) -> bool:
        return self.model.operable

    def is_selectable(self) -> bool:
        return self.model.selectable

    def is_show_index(self) -> bool:
        return self.model.show_index

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) or {}
        context.update({
            'model_name': self.model.__name__,
            'model_verbose_name': attr(self, 'model._meta.verbose_name'),
            'creatable': self.is_creatable(),
            'cloneable': self.is_cloneable(),
            'editable': self.is_editable(),
            'viewable': self.is_viewable(),
            'removable': self.is_removable(),
            'operable': self.is_operable(),
            'exportable': self.is_exportable(),
            "selectable": self.is_selectable(),
            "show_index": self.is_show_index(),
        })
        return context
