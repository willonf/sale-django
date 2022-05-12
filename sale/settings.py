"""
Django settings for sale project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
from corsheaders.defaults import default_methods

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-t&5$2#-@6mbri33+5qg9ak(sqm9u$e@_gr@6zq8-u%-hp(zvmw'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# TODO: host com permissão para acessar a API. Em ambiente deddesenvolvimento, pode-se deixar livre para todos
ALLOWED_HOSTS = ['*']

# Application definition

# TODO: Declaração de apps disponíveis para o projeto
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'basic.apps.BasicConfig',
    'django_filters',  # TODO: Django Filters setting
    'rest_framework',  # TODO: Django Rest setting
    'channels',  # TODO: Websocket setting
    'rest_framework.authtoken'  # TODO: Autenticação. Aplicar migrations
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # TODO: Configuração do Websocket
]

# TODO: Configuração do Websocket

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = default_methods

ROOT_URLCONF = 'sale.urls'

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

WSGI_APPLICATION = 'sale.wsgi.application'
ASGI_APPLICATION = 'sale.asgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

# TODO: campo onde configuramos o acesso ao banco de dados, de acordo o com o driver escolhido
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sale',
        'HOST': 'localhost',  # TODO: Alterar para serviço dentro do container no build da imagem
        'PORT': '5432',
        'USER': 'postgres',
        'PASSWORD': '123456'
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
# TODO: métodos de validação de senhas
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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['console'],
        },
        'django': {
            'level': 'INFO',
            'handlers': ['console'],
            # 'propagate': False
        },
        'django.request': {
            'level': 'DEBUG',
            'handlers': ['console'],
            # 'propagate': False
        }
    }
}
# TODO: Configuração de paginação automática do Rest Framework
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    # Configuração para retornar os valores numéricos como números e não como string
    'COERCE_DECIMAL_TO_STRING': False,
    # TODO: Django Filters backend setting
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
    ),
    # TODO: Classes utilizada para autenticações
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSIONS_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissions',
    ),
}

# TODO: Configuração do Celery
# '/0': database (do tipo chave-valor) padrão do Redis
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = 'America/Manaus'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

# TODO: Configuração do Websocket
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            # TODO: Alterar para serviço dentro do container no build da imagem. Ex.: redis
            'hosts': [('127.0.0.1', 6379)]
        }
    }
}

# TODO: Configuração de autenticação
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
)
