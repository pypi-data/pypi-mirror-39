from django.urls import reverse
from django.views.generic.edit import CreateView

from .form import AdminFormView


class AdminCreateView(AdminFormView, CreateView):
    success_message = "创建成功!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_action"] = reverse(f'{self.model.__name__}-create')
        context["view_type"] = 'create'

        return context
