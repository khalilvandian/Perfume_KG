"""
Django settings for paradise_papers_search project.

Generated by 'django-admin startproject' using Django 1.11.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from neomodel import config
from .env import env

#Connect to Neo4j Database
# config.DATABASE_URL = env('DATABASE_URL')  # default
# config.DATABASE_URL = 'bolt://neo4j:flames-throttle-cruiser@44.211.58.177:7687'

# config.DATABASE_URL = 'bolt://neo4j:Perfume_tmp@localhost:11003'
config.DATABASE_URL = 'bolt://neo4j:perfumeKG@localhost:7687'

# '''
# connecting to auraDB
# '''
# user = 'neo4j'
# psw = '1McmE-lDtVUMYBPUFsiQKscrqbD4M58Oc1hJOcKulcM'
# uri = '36d638c4.databases.neo4j.io'

# config.DATABASE_URL = 'neo4j+s://{}:{}@{}'.format(user, psw, uri)
# print(config.DATABASE_URL)




# DATABASES = {
#     'default': {
#         'NAME': 'papers.db',
#         'ENGINE': 'django.db.backends.sqlite3',
#         'USER': '',
#         'PASSWORD': '',
#         'PORT': '',
#     },
# }


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '7jvc876=)%+t5^k4p0qd^ysi@4317lo*r+ki^r3)e(*g-efh&^'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django_neomodel',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'fetch_api',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
]

ROOT_URLCONF = 'paradise_papers_search.urls'

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

WSGI_APPLICATION = 'paradise_papers_search.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Rest-Framework settings
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}
