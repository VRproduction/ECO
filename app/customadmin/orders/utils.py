from django.urls import reverse_lazy
from django.contrib.auth.mixins import AccessMixin


class SuperuserRequiredMixin(AccessMixin):
    """Mixin that allows only superusers to access the view."""

    login_url = reverse_lazy('admin:login')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
