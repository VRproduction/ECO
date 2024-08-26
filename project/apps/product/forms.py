from django import forms
from django.forms import ModelForm
from .models import Contact
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from django.utils.translation import gettext_lazy as _

User = get_user_model()

class ContactForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'number', 'subject', 'text', 'captcha']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Ad Soyad')}),
            'email': forms.EmailInput(attrs={'placeholder': _('Email')}),
            'number': forms.TextInput(attrs={'placeholder': _('Nömrə')}),
            'subject': forms.TextInput(attrs={'placeholder': _('Mövzu')}),
            'text': forms.Textarea(attrs={'placeholder': _('Mesaj')}),
        }

class AccountUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

   