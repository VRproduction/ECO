from django import forms
from django.forms import ModelForm
from .models import Contact
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

User = get_user_model()

class ContactForm(ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    class Meta:
        model = Contact
        fields = ['name', 'email', 'number', 'subject', 'text', 'captcha']


class AccountUpdateForm(UserChangeForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

   