from django.views.generic import TemplateView
import datetime

from apps.seo.models import  HomePageSeo
from apps.product.models import FAQ, Blog, ProductCategory, Product, Feature, Company, Partner, Statistic
from apps.pages.about.models import About
from apps.pages.home.models import IndexSlider, CategoryBanner


class HomePageView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context["sliders"] = IndexSlider.objects.all()
        context["categories"] = ProductCategory.objects.filter(is_active = True)
        context["products"] = Product.objects.filter(is_main_page = True,is_active = True, stock__gt=0).order_by("-badges")[:10]
        context["category_banners"] = CategoryBanner.objects.all()[:3]
        context["about"] = About.objects.first()
        context["features"] = Feature.objects.all()
        context["companies"] = Company.objects.filter(finish_time__gte=datetime.datetime.now())[:4]
        context["most_selling_products"] = Product.objects.filter(is_best_seller = True,is_active = True).order_by("?")[:3]
        context["most_search_products"] = Product.objects.filter(is_most_wonted = True,is_active = True).order_by("?")[:3]
        context["trending_products"] = Product.objects.filter(is_trending = True,is_active = True).order_by("?")[:3]
        context["partners"] = Partner.objects.all()
        context["statistic"] = Statistic.objects.first()
        context["faqs"] = FAQ.objects.all()
        context["blogs"] = Blog.objects.filter(is_main_page = True)[:3]
        context["seo"] = HomePageSeo.objects.first()
        return context