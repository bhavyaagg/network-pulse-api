"""
Django settings for pulseapi project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import dj_database_url
import environ

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

app = environ.Path(__file__) - 1
root = app - 1

environ.Env.read_env(os.path.join(BASE_DIR, '.env'))
env = environ.Env(
    DEBUG=(bool, False),
    USE_S3=(bool, False),
    SSL_PROTECTION=(bool, False),
    CORS_REGEX_WHITELIST=(tuple, ()),
    PULSE_FRONTEND_HOSTNAME=(str, ''),
)
SSL_PROTECTION = env('SSL_PROTECTION')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')
ALLOW_UNIVERSAL_LOGIN = env('ALLOW_UNIVERSAL_LOGIN', default=None)

# This needs to be a real domain for google auth purposes. As such,
# you may need to add a "127.0.0.1    test.example.com" to your
# host file, so that google's redirect works. This is the same
# domain you will be specifying in your Flow credentials, and
# associated client_secrets.json
ALLOWED_HOSTS = os.getenv(
    'ALLOWED_HOSTS',
    'test.example.com,localhost,network-pulse-api-staging.herokuapp.com,network-pulse-api-production.herokuapp.com'
).split(',')

SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 31
SECRET_KEY = 'Oh my god I love cake so much holy shit how amazing is cake; like, seriously?'

# Application definition
SITE_ID = 1

INSTALLED_APPS = list(filter(None, [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'storages',
    'pulseapi.entries',
    'pulseapi.tags',
    'pulseapi.issues',
    'pulseapi.helptypes',
    'pulseapi.users',
    'pulseapi.profiles',
    'pulseapi.creators',
    # see INTERNAL_IPS for when this actually activates when DEBUG is set:
    'debug_toolbar' if DEBUG is True else None,
]))

MIDDLEWARE = list(filter(None, [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # see INTERNAL_IPS for when this actually activates when DEBUG is set:
    'debug_toolbar.middleware.DebugToolbarMiddleware' if DEBUG is True else None,
]))

# Whitelisting for the debug toolbar: it will not kick in except for when
# accessed through the following domains ("IP" is a white lie, here).
INTERNAL_IPS = [
    'localhost',
    '127.0.0.1',
]

AUTH_USER_MODEL = 'users.EmailUser'

ROOT_URLCONF = 'pulseapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pulseapi.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASE_URL = os.getenv('DATABASE_URL', False)

if DATABASE_URL is not False:
    DATABASES['default'].update(dj_database_url.config())


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


#
# CORS settings
#

# we want to restrict API calls to domains we know
CORS_ORIGIN_ALLOW_ALL = False

# we also want cookie data, because we use CSRF tokens
CORS_ALLOW_CREDENTIALS = True

# and we want origin whitelisting
CORS_ORIGIN_WHITELIST = os.getenv(
    'CORS_ORIGIN_WHITELIST',
    'localhost:3000,localhost:8000,localhost:8080,test.example.com:8000,test.example.com:3000'
).split(',')

CORS_ORIGIN_REGEX_WHITELIST = env('CORS_REGEX_WHITELIST')

CSRF_TRUSTED_ORIGINS = CORS_ORIGIN_WHITELIST
CSRF_COOKIE_HTTPONLY = env('CSRF_COOKIE_HTTPONLY', default=SSL_PROTECTION)
CSRF_COOKIE_SECURE = env('CSRF_COOKIE_SECURE', default=SSL_PROTECTION)
SECURE_BROWSER_XSS_FILTER = env('SECURE_BROWSER_XSS_FILTER', default=SSL_PROTECTION)
SECURE_CONTENT_TYPE_NOSNIFF = env('SECURE_CONTENT_TYPE_NOSNIFF', default=SSL_PROTECTION)
SECURE_HSTS_INCLUDE_SUBDOMAINS = env('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=SSL_PROTECTION)
SECURE_HSTS_SECONDS = 60*60*24*31*6
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=SSL_PROTECTION)
SESSION_COOKIE_SECURE = env('SESSION_COOKIE_SECURE', default=SSL_PROTECTION)

# Heroku goes into an infinite redirect loop without this. So it's kind of necessary.
# See https://docs.djangoproject.com/en/1.10/ref/settings/#secure-ssl-redirect
if SSL_PROTECTION is True:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

X_FRAME_OPTIONS = "DENY"

# Frontend URL is required for the RSS and Atom feeds
PULSE_FRONTEND_HOSTNAME = env('PULSE_FRONTEND_HOSTNAME')

USE_S3 = env('USE_S3')

if USE_S3:
    # Use S3 to store user files if the corresponding environment var is set
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = env('AWS_S3_CUSTOM_DOMAIN')
    AWS_LOCATION = env('AWS_STORAGE_ROOT', default=None)
else:
    # Otherwise use the default filesystem storage
    MEDIA_ROOT = root('media/')
    MEDIA_URL = '/media/'
