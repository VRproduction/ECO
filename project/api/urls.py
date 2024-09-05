from django.urls import path, include

urlpatterns = [
    path("support/", include("api.support.urls")),
    path("chat_bot/", include("api.chat_bot.urls"))
]
