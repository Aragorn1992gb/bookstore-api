"""
Django settings for bookstore_api project.

Generated by 'django-admin startproject' using Django 4.2.9.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-q1bvfhhb0s5812-!8to1gy6jtw%%^dd1qw+a=iq=64zqq27(dc'

# SECURITY WARNING: don't run with debug turned on in production!
if os.environ.get("PROJECT_ENV") == "prod":
    DEBUG = False
else:
    DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'drf_yasg',
    'corsheaders',
    'dj_rest_auth',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'book'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # for staticfiles when DEBUG = False
]

ROOT_URLCONF = 'bookstore_api.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'bookstore_api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'HOST': os.environ.get('DB_HOST'),
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'ATOMIC_REQUESTS': True
        # 'PORT': '5432',
    },

    # "nonrel": {
    #     "ENGINE": "djongo",
    #     "NAME": os.environ.get('MONGO_DB_NAME'),
    #     "CLIENT": {
    #         "host": os.environ.get('MONGO_DB_HOST'),
    #         "port": 27017,
    #         "username": os.environ.get('MONGO_DB_USERNAME'),
    #         "password": os.environ.get('MONGO_DB_PASSWORD'),
    #     },
    #     'TEST': {
    #         'MIRROR': 'default',
    #     },
    # }

    # "mongo": {
    #     "ENGINE": "djongo",
    #     "NAME": os.environ.get('MONGO_DB'),
    #     "CLIENT": {
    #         "host": os.environ.get('MONGO_HOST'),
    #         "port": 27017,
    #         "username": os.environ.get('MONGO_USER'),
    #         "password": os.environ.get('MONGO_PASSWORD'),
    #     },
    #     'TEST': {
    #         'MIRROR': 'default',
    #     },
    # }
}

DJONGO_DATABASES = {
    'default': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('MONGO_DB'),
        'USER': os.environ.get('MONGO_USER'),
        'PASSWORD': os.environ.get('MONGO_PASSWORD'),
        'HOST': os.environ.get('MONGO_HOST'),
    },
    'mongo': {
        'ENGINE': 'djongo',
        'NAME': os.environ.get('MONGO_DB'),
        'USER': os.environ.get('MONGO_USER'),
        'PASSWORD': os.environ.get('MONGO_PASSWORD'),
        'HOST': os.environ.get('MONGO_HOST'),
    },
}

# DJONGO_DATABASES = {
#     'default': {
#         'ENGINE': 'djongo',
#         'NAME': 'your_mongo_database_name',
#     },
#     'mongo': {
#         'ENGINE': 'djongo',
#         'NAME': 'your_mongo_database_name',
#     },
# }


SWAGGER_SETTINGS = {
   'USE_SESSION_AUTH': False,
   'SECURITY_DEFINITIONS': {
     'Token': {
       'type': 'apiKey',
       'name': 'Authorization',
       'in': 'header'
     }
   }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_ROOT = BASE_DIR / 'staticfiles'

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # 'var/www/static/'
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
