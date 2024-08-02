from .models import About
from modeltranslation.translator import TranslationOptions,register

@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

