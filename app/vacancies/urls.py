from django.urls import path, include
from .views import (
    VacancyListView,
    VacancyDetailView
)

urlpatterns = [
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('vacancies/<str:slug>/', VacancyDetailView.as_view(), name='vacancy-detail')
]