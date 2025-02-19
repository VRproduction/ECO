from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Append the BrowserReloadMiddleware only in local environment
MIDDLEWARE += [
    # "django_browser_reload.middleware.BrowserReloadMiddleware",
]

INSTALLED_APPS += [
    'django_browser_reload'
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'sales@ecoproduct.az'  
EMAIL_HOST_PASSWORD = 'nkepqjrjsjwjnosz'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
# DEFAULT_FROM_EMAIL = 'turalabbaszade2022@gmail.com' #test
DEFAULT_FROM_EMAIL = 'ilqarhesenov2003@gmail.com' #test