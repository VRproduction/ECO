from .models import Product, GeneralSettings, IndexSlider, ProductCategory, Vendor, CategoryBanner, About, Feature, Partner, FAQ, Blog
from modeltranslation.translator import TranslationOptions,register

@register(GeneralSettings)
class GeneralSettingsTranslationOptions(TranslationOptions):
    fields = ('site_title', 'adress', 'footer_slogan', 'copyright_title')

@register(IndexSlider)
class IndexSliderTranslationOptions(TranslationOptions):
    fields = ('title', 'mobile_title', 'description', 'mobile_description')


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Vendor)
class VendorTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords', 'meta_description')

@register(CategoryBanner)
class CategoryBannerTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(About)
class AboutTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Feature)
class FeatureTranslationOptions(TranslationOptions):
    fields = ('title1', 'title2')

@register(Partner)
class PartnerTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(FAQ)
class FAQTranslationOptions(TranslationOptions):
    fields = ('title', 'description')

@register(Blog)
class BlogTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords', 'meta_description')