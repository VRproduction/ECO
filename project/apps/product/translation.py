from .models import Product, ProductCategory, Vendor, Feature, Partner, FAQ, Blog
from modeltranslation.translator import TranslationOptions,register


@register(ProductCategory)
class ProductCategoryTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Vendor)
class VendorTranslationOptions(TranslationOptions):
    fields = ('title',)

@register(Product)
class ProductTranslationOptions(TranslationOptions):
    fields = ('title', 'description', 'keywords', 'meta_description')

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