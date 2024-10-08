from django.contrib import admin
from django.urls import path, include, re_path
from . import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap
from .sitemap import StaticSitemap, BlogSitemap, ProductSitemap
from django.views.static import serve
from django.views.generic import TemplateView

from django.conf.urls.i18n import i18n_patterns
from urllib.parse import urlparse
from django.conf import settings
from django.http import HttpResponseRedirect
from django.urls.base import resolve, reverse
from django.urls.exceptions import Resolver404
from django.utils import translation

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

sitemaps = {
    # 'static': StaticSitemap,
    'blog': BlogSitemap,
    'service': ProductSitemap,
}

def set_language(request, language):
    for lang, _ in settings.LANGUAGES:
        translation.activate(lang)
        try:
            view = resolve(urlparse(request.META.get("HTTP_REFERER")).path)
        except Resolver404:
            view = None
        if view:
            break
    if view:
        translation.activate(language)
        next_url = reverse(view.url_name, args=view.args, kwargs=view.kwargs)
        response = HttpResponseRedirect(next_url)
        response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    else:
        response = HttpResponseRedirect("/")
    return response

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('web.urls')),
    # path('', include('apps.pages.home.urls')),
    path('', include('apps.product.urls')),
    path('', include('apps.vacancies.urls')),
    path('api/', include('apps.vacancies.api.urls')),
    path('api/v1/', include('api.urls')),
    path('custom-admin/', include('apps.customadmin.urls')),
    path('account/', include('apps.account.urls')),
    path('payment/', include('apps.payment.urls')),
    path('wolt/', include('apps.wolt.urls')),
    path('sitemap.xml', sitemap, {
      'sitemaps': sitemaps,
      'template_name': 'custom-sitemap.html'
    }, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt/', TemplateView.as_view(template_name='robots.txt', content_type="text/plain")),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),


    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    re_path('^rosetta', include("rosetta.urls")),
    path("__reload__/", include("django_browser_reload.urls")),
]

urlpatterns = [
    *i18n_patterns(*urlpatterns, prefix_default_language=False),
    path("set_language/<str:language>", set_language, name="set-language"),

    ]


if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^translation/', include('rosetta.urls'))
    ]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# urlpatterns += staticfiles_urlpatterns()
