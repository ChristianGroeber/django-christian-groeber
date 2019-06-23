"""
Django settings for christian_groeber_ch project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import json
import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from oauth2client.service_account import ServiceAccountCredentials

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$-kv9ft*8c@on$p$j55qn!uysijsi2f-#ypcrnz(1*)y71o4(='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['christiangroeber.pythonanywhere.com', '127.0.0.1', 'www.christian-groeber.ch']


# Application definition

INSTALLED_APPS = [
    'work_tracker',
    'martor',
    'blog',
    'hire_me',
    'colorfield',
    'website',
    'portfolio',
    'contact',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'froala_editor',
    'social_django',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'christian_groeber_ch.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'website.context_processors.pages',
                'website.context_processors.social_media',
                'social_django.context_processors.backends',  # <- Here
                'social_django.context_processors.login_redirect',  # <- Here
            ],
        },
    },
]

WSGI_APPLICATION = 'christian_groeber_ch.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.open_id.OpenIdAuth',  # for Google authentication
    'social_core.backends.google.GoogleOpenId',  # for Google authentication
    'social_core.backends.google.GoogleOAuth2',  # for Google authentication

    'django.contrib.auth.backends.ModelBackend',
)

with open('client_secret_240082627833-thcll2e8hukf2hb2sngvass639er6ho1.apps.googleusercontent.com.json', 'r') as f:
    datastore = json.load(f)

SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = datastore['web']['client_secret']
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = datastore['web']['client_id']


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Zurich'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

MEDIA_URL = '/media/'

SETTINGS_PATH = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DIRS = (
    os.path.join(SETTINGS_PATH, 'templates'),
)

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(SETTINGS_PATH, "static"),
]


STATIC_ROOT = 'static_cdn'
MEDIA_ROOT = 'media_cdn'
