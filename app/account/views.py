from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout, login
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.tokens import default_token_generator
from .utils.login_helper import AuthView, IsNotAuthView
from .forms import RegisterForm, RememberMeAuthenticationForm
from .models import LoginRegisterPage

from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

from django.contrib.auth import get_user_model

from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
)
from django.utils.translation import gettext_lazy as _

from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetConfirmView
from django.urls import reverse

User = get_user_model()

class RegisterSuccessView(TemplateView):
    template_name = 'register_success.html'



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
    success_url = reverse_lazy("register_success")

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.set_unusable_password()  # Set unusable password until email is verified
        self.object.is_active = False  
        self.object.save()
        token = default_token_generator.make_token(self.object)
        
        verification_url = self.request.build_absolute_uri(
            reverse_lazy("verify_email", kwargs={"uidb64": urlsafe_base64_encode(force_bytes(self.object.pk)), "token": token})
        )
        subject = "E-poçt ünvanınızı yoxlayın"
        message = render_to_string("mail/email_verification.html", {"verification_url": verification_url})
        send_mail(subject, message, settings.EMAIL_HOST_USER, [self.object.email],html_message=message)
        return redirect(self.get_success_url())


    def get_context_data(self, **kwargs):
        context = super(CustomRegisterView, self).get_context_data(**kwargs)
        context["register_page"] = LoginRegisterPage.objects.first()
        return context
    
def logout_view(request):
    logout(request)
    return redirect('login')

from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode

def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_email_verified = True
        user.is_active = True  
        user.save()
        login(request, user)
        return redirect('home')  
    else:
        return redirect('invalid_token') 
    


def custom_password_reset(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.get(email=email)  # Kullanıcıyı bulun
            token = default_token_generator.make_token(user)  # Token oluştur
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))  # Kullanıcı kimliğini base64'e çevir
            reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token}))  # Şifre sıfırlama URL'sini oluştur
            send_mail(
                'Ecoproduct.az, şifrə sıfırlama',
                f'Şifrənizi sıfırlamaq üçün lütfən bu linkə keçid edin: {reset_url}',
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
            )
            messages.success(request, 'Şifre sıfırlama bağlantısı e-posta adresinize gönderildi.')
            return redirect('password_reset_done')
    else:
        form = PasswordResetForm()
    return render(request, 'password_reset.html', {'form': form})

def custom_password_reset_done(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'password_reset_done.html')

class CustomPasswordResetConfirmView(PasswordResetConfirmView, AuthView):
    template_name = 'password_reset_confirm.html'  

    def get(self, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

def custom_password_reset_complete(request):
    if request.user.is_authenticated:
        return redirect("home")
    return render(request, 'password_reset_complete.html')