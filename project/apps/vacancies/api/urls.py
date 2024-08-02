from django.urls import path

from .views import VacancyPostAPIView

urlpatterns = [
    path('vacancy/', VacancyPostAPIView.as_view(), name='vacancy')
]