from django.urls import path, include
from .views.faq import FAQListView

urlpatterns = [
    path("faqs/", FAQListView.as_view(), name = 'faqs')
]
