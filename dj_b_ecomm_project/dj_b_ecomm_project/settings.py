
from pathlib import Path
import os
from django.utils.translation import gettext_lazy as _
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = 'django-insecure-z#emb=ibo*4%*ofql$6k6-&)9zudvbv1jye+xk1c@%x3e265rx'


DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'modeltranslation',
    'apps.cart',
    'apps.core',
    'apps.orders',
    'apps.shop',
    'widget_tweaks',
    "rosetta",
    'apps.accounts.apps.AccountsConfig',


    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.openid_connect',


]



SOCIALACCOUNT_PROVIDERS = {
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "linkedin",
                "name": "LinkedIn",
                "client_id": config("LINKEDIN_CLIENT_ID"),
                "secret": config("LINKEDIN_CLIENT_SECRET"),
                "settings": {
                    "server_url": "https://www.linkedin.com/oauth",
                },
            }
        ]
    }
}

MIDDLEWARE = [
    'allauth.account.middleware.AccountMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
     "django.middleware.locale.LocaleMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',


    # Block User Middleware
    "apps.accounts.middlewares.block_check.BlockCheckMiddleware",
]

ROOT_URLCONF = 'dj_b_ecomm_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.shop.context_processors.cart_context',
                'django.template.context_processors.request',

            ],
        },
    },
]

SITE_ID = 1


AUTHENTICATION_BACKENDS = [
    'apps.accounts.backends.EmailBackend',   # our custom backend
    'django.contrib.auth.backends.ModelBackend',  # default
    'allauth.account.auth_backends.AuthenticationBackend', # all auth backend

]



LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_LOGIN_ON_GET = True


AUTH_USER_MODEL = "accounts.CustomUser"

WSGI_APPLICATION = 'dj_b_ecomm_project.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




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


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ("en", _("English")),
    ("fr", _("French")),
    ("hi", _("Hindi")),
    ("pa", _("Punjabi")),
]

MODELTRANSLATION_DEFAULT_LANGUAGE = 'en'
MODELTRANSLATION_LANGUAGES = ('en', 'fr', 'hi', 'pa')

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Add project-level static folder
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST_USER = config('GMAIL_ADDRESS')         # e.g. 'youremail@gmail.com'
EMAIL_HOST_PASSWORD = config('GMAIL_APP_PASSWORD')# the 16-char App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


SITE_URL = "http://127.0.0.1:8000"