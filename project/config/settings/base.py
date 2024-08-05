import os

from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv(
    'DJANGO_SECRET_KEY',
    'django-insecure-d)-9&oks3j52p0m0-tn#i)zmc(z$g0o24ls9^gxnfujdik_+*#'
)
# Application definition

INTERNAL_API_KEYS = [
    '52b4e6a4-f4c4-4b56-91a6-0fc198c6a680',
    'eecb82af-983d-4a12-9acd-a17dda60f42c',
]

EXTERNAL_API_KEYS = [
    '8996d602-8c6c-4f4a-ae4e-fb2fe32ea090',
    '5df8a8f5-0595-47c8-a87f-011c17f94cf1',
]


SITE_ID = 1

DJANGO_APPS = [
    'modeltranslation',#new
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', #new
    'django.contrib.sites', #new
]

CUSTOM_APPS = [
    'apps.config.apps.ConfigConfig',
    'apps.core.apps.CoreConfig',
    'apps.product.apps.ProductConfig',
    'apps.account.apps.AccountConfig',
    'apps.payment.apps.PaymentConfig',
    'apps.wolt.apps.WoltConfig',
    'apps.seo.apps.SeoConfig',
    'apps.vacancies.apps.VacanciesConfig',
    'apps.customadmin.apps.CustomadminConfig',

    #pages
    'apps.pages.home.apps.HomeConfig',
    'apps.pages.about.apps.AboutConfig',
]

THIRD_PARTY_APPS = [
    'ckeditor',
    'rest_framework',
    'rosetta',
    "corsheaders",

    "django_celery_results",
    "django_celery_beat",

    'drf_yasg',
    'drf_spectacular',
    'drf_spectacular_sidecar',  # optional - provides swagger-ui and redoc

]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS


FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware", #new
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware', #new
    "corsheaders.middleware.CorsMiddleware", #new
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

CORS_ALLOW_ALL_ORIGINS = True

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'utils.context_processors.extras.extras',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'account.CustomUser'

LOGIN_URL = '/account/login/'
LOGOUT_REDIRECT_URL = '/'


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]


LANGUAGE_CODE = 'az'

TIME_ZONE = 'Asia/Baku'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('az', _('Azerbaijani')),
    ('ru', _('Russian')),
    ('en', _('English')),
)

# MODELTRANSLATION_DEFAULT_LANGUAGE = 'az'
MODELTRANSLATION_LANGUAGES = ('az', 'en', 'ru')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS=[os.path.join(BASE_DIR,'static/')]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

CKEDITOR_CONFIGS = {
    'default':
        {
            'toolbar': 'full',
            'width': 'auto',
            'extraPlugins': ','.join([
                'codesnippet',
            ]),
        },
}

WOLT_API_KEY_TEST = "PUNlJQGSVyqo8ShrDCd4uULMfzviPh8V5ywt6LdjYIY"
WOLT_VENUE_ID_TEST = "65cf2245fc643985912ab003"
WOLT_MERCHANT_ID_TEST = "65cf21d501026216134fd3c6"

WOLT_API_KEY = "3kyk_bFdujIdtqYU4X41cTas99GZdyNKDgAIUlvQpOw"
WOLT_VENUE_ID = "65f996bad734c57402f32d74"
WOLT_MERCHANT_ID = "65f9947d5474cf86a0afde68"



#for storing result
CELERY_RESULT_BACKEND = 'django-db'
# CELERY_RESULT_BACKEND = "redis://localhost:6379/0"

#SETTINGS FOR CELERY

CELERY_BROKER_URL='redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT=['application/json']
CELERY_RESULT_SERIALIZER='json'
CELERY_TASK_SERIALIZER='json'

CELERY_BEAT_SCHEDULER='django_celery_beat.schedulers:DatabaseScheduler'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,

    'DEFAULT_SCHEMA_CLASS': 'utils.api.swagger.schemas.CustomAutoSchema',
    # 'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',

}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Ecoproduct API docs',
    'DESCRIPTION': 'My API description',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    # 'SERVE_PERMISSIONS': ['rest_framework.permissions.IsAuthenticated'],
    'PREPROCESSING_HOOKS': [
        'utils.api.swagger.hooks.filter_endpoints',  # Hook function for filtering endpoints
        # 'utils.api.swagger.hooks.add_accept_language_header',  # Hook function for filtering endpoints
    ],
    'POSTPROCESSING_HOOKS': [],
}