from .models import IndexSlider, CategoryBanner
from modeltranslation.translator import TranslationOptions,register

@register(IndexSlider)
class IndexSliderTranslationOptions(TranslationOptions):
    fields = ('title', 'mobile_title', 'description', 'mobile_description')

@register(CategoryBanner)
class CategoryBannerTranslationOptions(TranslationOptions):
    fields = ('title',)