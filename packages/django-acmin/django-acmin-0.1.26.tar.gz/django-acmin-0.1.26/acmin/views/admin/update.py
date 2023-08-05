from django.urls import reverse
from django.views.generic.edit import UpdateView

from .form import AdminFormView


class AdminUpdateView(AdminFormView, UpdateView):
    success_message = "更新成功!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_clone = self.request.GET.get("clone") is not None
        context['form_action'] = self.get_object().get_absolute_url()
        context["view_type"] = 'update'
        if is_clone:
            obj = context["object"]
            obj.id = ""
            context["form_action"] = reverse(f'{self.model.__name__}-create')
        return context
