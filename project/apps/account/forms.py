from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox
from django.utils.translation import gettext_lazy as _


User = get_user_model()

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        widget=forms.TextInput(attrs={'autofocus': True, 'placeholder':'Email *'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'Parol *'}),
    )
    error_messages = {
        'invalid_login': "Düzgün email və password daxil edin!",
    }

class RememberMeAuthenticationForm(EmailAuthenticationForm):
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    )

class RegisterForm(UserCreationForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)  
    first_name = forms.CharField(
        max_length=30, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': _('Ad')})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False, 
        widget=forms.TextInput(attrs={'placeholder': _('Soyad')})
    )
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': 'Email *'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'Parol *'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'Parol yenidən *'}),
        }