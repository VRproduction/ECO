from django.urls import path

from .home.views import HomePageView

urlpatterns = [
    path('dev/', HomePageView.as_view(), )
]