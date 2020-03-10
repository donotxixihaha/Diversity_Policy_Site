"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import django_heroku 
import dj_database_url

config = dj_database_url.config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'seq5*nc-h#yrb4q-14h^fegrd_bx@v#(l#a^!%h(4s8f05kjrw'
DEBUG = True

# Experimenting here
ALLOWED_HOSTS = ["localhost", "https://stormy-stream-43261.herokuapp.com/"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'website',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
    
]

ROOT_URLCONF = 'DP_site.urls'

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

WSGI_APPLICATION = 'DP_site.wsgi.application'


# from django.core.exceptions import ImproperlyConfigured
 
# def get_env_variable(var_name):
#     try:
#         return os.environ[var_name]
#     except KeyError:
#         error_msg = "Set the %s environment variable" % var_name
#         raise ImproperlyConfigured(error_msg)

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# one for development (maybe move that to local postgres) and another for running and development
DATABASES = {

    # 'default': {
    #    'ENGINE': 'django.db.backends.postgresql',
    #    'NAME': 'xsboediz',
    #    'USER': 'xsboediz',
    #    'PASSWORD': 'Qcn3tmpnSgp1QHgk_dsCvukFFPJAofm0',
    #    'HOST': 'baasu.db.elephantsql.com',
    #    'PORT': '5432'
    # }

    'default': {
       'ENGINE': 'django.db.backends.postgresql',
       'NAME': 'dec8d7tivikhbg',
       'USER': 'ucdeqrj57q3flv',
       'PASSWORD': 'pd66f2f9fcd34c0363c86e8835c2a52baacc2bfcba7d0720ee9f0ff1ab48d584e',
       'HOST': 'ec2-3-81-238-195.compute-1.amazonaws.com',
       'PORT': '5432'
    }

    #
    # 'default': dj_database_url.config(
    #     default=config('DATABASE_URL')
    # )
    #

    # 'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': 'mydatabase',
    #     }


}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#STATIC_URL = './staticfiles/'
STATIC_URL = '/static/'

# STATICFILES_DIRS = (
#     #'/Diversity_Policy_Site/blog/static',
#     os.path.join(BASE_DIR, '/static/'),
# )
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'

django_heroku.settings(locals())
