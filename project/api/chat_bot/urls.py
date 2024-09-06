from django.urls import path, include
from .views.faq import FAQListView
from .views.chat_link import ChatLinkView

urlpatterns = [
    path("faqs/", FAQListView.as_view(), name = 'faqs'),
    path("chat-link/", ChatLinkView.as_view(), name = 'chat-link')
]
