from django.urls import path, include

urlpatterns = [
    path("support/", include("api.support.urls"))
]
