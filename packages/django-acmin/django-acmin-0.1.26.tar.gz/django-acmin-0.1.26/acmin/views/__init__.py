from .admin import (
    AdminCreateView, AdminDeleteView, AdminExportView, AdminFormView, AdminListView, StaticFilterMixin, AdminUpdateView
)
from .admin import get_view as get_admin_view
from .view import ApiView, route, admin_route, WebView, url, get_urlpatterns
