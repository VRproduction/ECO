from .models.general_settings import  GeneralSettings
from modeltranslation.translator import TranslationOptions,register

@register(GeneralSettings)
class GeneralSettingsTranslationOptions(TranslationOptions):
    fields = ('site_title', 'adress', 'footer_slogan', 'copyright_title')

