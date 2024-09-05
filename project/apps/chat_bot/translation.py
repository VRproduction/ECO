from .models import FAQCategory, FAQ
from modeltranslation.translator import TranslationOptions,register


@register(FAQCategory)
class FAQCategoryTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('question', 'answer')