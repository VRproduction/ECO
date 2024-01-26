from django.views.generic import TemplateView
from .models import FAQ, Blog, IndexSlider, ProductCategory, Product, CategoryBanner, About, Feature, Company, Partner, Statistic

class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["sliders"] = IndexSlider.objects.all()[:2]
        context["categories"] = ProductCategory.objects.all()
        context["products"] = Product.objects.all()[:9]
        context["category_banners"] = CategoryBanner.objects.all()[:3]
        context["about"] = About.objects.first()
        context["features"] = Feature.objects.all()
        context["companies"] = Company.objects.filter(is_active = True)[:4]
        context["most_selling_products"] = Product.objects.all().order_by("?")[:3]
        context["most_search_products"] = Product.objects.all().order_by("?")[:3]
        context["trending_products"] = Product.objects.all().order_by("?")[:3]
        context["partners"] = Partner.objects.all()
        context["statistic"] = Statistic.objects.first()
        context["faqs"] = FAQ.objects.all()
        context["blogs"] = Blog.objects.filter(is_main_page = True)[:3]
        return context