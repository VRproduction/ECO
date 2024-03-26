from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name = "login"),
    path('register/', views.CustomRegisterView.as_view(), name = "register"),
    path('register-success/', views.RegisterSuccessView.as_view(), name = "register_success"),
    path('logout/', views.logout_view, name = "logout"),
    path('verify-email/<uidb64>/<token>/', views.verify_email, name='verify_email'),
    
    path('password-reset/', views.custom_password_reset, name='password_reset'),
    path('password-reset/done/', views.custom_password_reset_done, name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset-complete/', views.custom_password_reset_complete, name='password_reset_complete'),
]