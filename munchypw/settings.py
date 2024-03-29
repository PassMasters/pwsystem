"""
Django settings for munchypw project.

Generated by 'django-admin startproject' using Django 4.2.3.

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
SECRET_KEY = 'django-insecure-k!%yar*k##2)(2t*=tzws#awfm+u+&tzbgp@o@lk#-uo^k^=&6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = ['https://munchysecurealpha.adaptable.app','https://cs947939-congenial-space-doodle-qprwjwprj7cxwg4-8000.preview.app.github.dev']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'pwmanager',
     'administrative',
     'security',
       # Enable allauth.
   'allauth',
    'allauth.socialaccount',
  'allauth.account',
  'lisence',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
 
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
     'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'munchypw.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": ['templates'],
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

WSGI_APPLICATION = 'munchypw.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

STUPID_SSL_CERT = os.path.join(BASE_DIR,"ca1.pem")



DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'ps4',
    'USER': 'fluffy',
    'PASSWORD': 'djhf9uasdfiuasfh#*(UVHEF(*CVBEf{}_++ji(()J()RR',
    'HOST': 'fluffyindustriesmaindb2.postgres.database.azure.com',
    'PORT': '5432',
  },
  #JUNK!
  
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
FIELD_ENCRYPTION_KEY = b'7pnYWOoWeqrShs9URzZXqlsU8gE802xFrJnlX3a1d8I='

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

AUTHENTICATION_BACKENDS = [
   
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
    
]
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
#STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),

)
#LOGIN_URL = "kagi:login"
# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
DEFAULT_FILE_STORAGE = 'pwmanager.s3.MediaStorage'
AWS_S3_REGION_NAME = 'us-west-004'
AWS_S3_ENDPOINT_URL = 'https://s3.us-west-004.backblazeb2.com'
#keys may be out of date

AWS_ACCESS_KEY_ID = '004a9e81991c2860000000001'
AWS_SECRET_ACCESS_KEY = 'K004XByq9AqVXOrCDoHAsTfv3DiFC3I'

EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = 'apikey' # this is exactly the value 'apikey'

EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'fluffy@fluffyindustries.tk'

ACCOUNT_SIGNUP_REDIRECT_URL = '/accounts/login?next=/passwords/setup'
LOGIN_REDIRECT_URL = '/passwords/munchy'

SITE_ID = 4
