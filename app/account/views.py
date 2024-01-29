from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views.generic import CreateView

from .utils.login_helper import AuthView
from .forms import RegisterForm, RememberMeAuthenticationForm
from .models import LoginRegisterPage

class CustomLoginView(AuthView, LoginView):
    form_class = RememberMeAuthenticationForm
    template_name = 'login.html'  

    def get_success_url(self) -> str:
        return reverse_lazy("home")
    
    def get_context_data(self, **kwargs):
        context = super(CustomLoginView, self).get_context_data(**kwargs)
        context["login_page"] = LoginRegisterPage.objects.first()
        return context
    
    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')
        if not remember_me:
            self.request.session.set_expiry(0)  
        return super().form_valid(form)
    

class CustomRegisterView(AuthView,CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        to_return = super().form_valid(form)
        login(self.request, self.object)
        return to_return


    def get_context_data(self, **kwargs):
        context = super(CustomRegisterView, self).get_context_data(**kwargs)
        context["register_page"] = LoginRegisterPage.objects.first()
        return context
    
def logout_view(request):
    logout(request)
    return redirect('login')

