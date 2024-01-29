from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import generic

class AuthView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse_lazy("home"))
        return super(AuthView, self).dispatch(request, *args, **kwargs)
    
class IsNotAuthView(generic.View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse_lazy("login"))
        return super(IsNotAuthView, self).dispatch(request, *args, **kwargs)