"""
Django settings for meHungry_project project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g-ziv_eq=p*sqeb$*k@w!u8bihnp-*n=p^_9&sbcmq$d(q-4*8'

from urlparse import urlparse, uses_netloc

##############---- STRIPE SETTINGS ----###################################################

# Site ID

SITE_ID=1

#Link to Docs :http://django-stripe-payments.readthedocs.org/en/latest/installation.html#configuration-modifications-to-settings-py

# Stripe Keys
STRIPE_PUBLIC_KEY= os.environ.get('STRIPE_PUBLIC_KEY',"pk_test_xDKTfOPxaGQBk3o3QOYUsVuJ")
STRIPE_SECRET_KEY=os.environ.get('STRIPE_SECRET_KEY',"sk_test_QOyWGJcHtngXcQNyyu5y8o52")



# Payment Plans (Needed to initialize stripe)
PAYMENTS_PLANS = {
    "monthly": {
        "stripe_plan_id": "pro-monthly",
        "name": "Web App Pro ($25/month)",
        "description": "The monthly subscription plan to WebApp",
        "price": 25,
        "currency": "usd",
        "interval": "month"
    },
    "yearly": {
        "stripe_plan_id": "pro-yearly",
        "name": "Web App Pro ($199/year)",
        "description": "The annual subscription plan to WebApp",
        "price": 199,
        "currency": "usd",
        "interval": "year"
    },
    "monthly-trial": {
        "stripe_plan_id": "pro-monthly-trial",
        "name": "Web App Pro ($25/month with 30 days free)",
        "description": "The monthly subscription plan to WebApp",
        "price": 25,
        "currency": "usd",
        "interval": "month",
        "trial_period_days": 30
    },
}

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'meHungry_customer_website',
    'carton',
    'django_forms_bootstrap',
    'payments',
    'social.apps.django_app.default',
    'ajax_select'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
   'django.contrib.auth.context_processors.auth',
   'django.core.context_processors.debug',
   'django.core.context_processors.i18n',
   'django.core.context_processors.media',
   'django.core.context_processors.static',
   'django.core.context_processors.tz',
   'django.contrib.messages.context_processors.messages',
   'social.apps.django_app.context_processors.backends',
   'social.apps.django_app.context_processors.login_redirect',
)

AUTHENTICATION_BACKENDS = (
   'social.backends.facebook.FacebookOAuth2',
   'social.backends.google.GoogleOAuth2',
   'social.backends.twitter.TwitterOAuth',
   'django.contrib.auth.backends.ModelBackend',
)

'''# Social Auth specific settings
SOCIAL_AUTH_DEFAULT_USERNAME = 'new_social_auth_user'
SOCIAL_AUTH_UID_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_HANDLE_LENGTH = 16
SOCIAL_AUTH_NONCE_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ASSOCIATION_SERVER_URL_LENGTH = 16
SOCIAL_AUTH_ENABLED_BACKENDS = ('google',)'''

# Google Auth Keys
SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = "887299565368-e8s4hpga4khhc7e6trg2jlk0gdnai8n6.apps.googleusercontent.com"
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = "pd9jngULVPkqS_P7Zmwax8Ez"


# LOGIN URLS
LOGIN_URL          = '/'
LOGIN_REDIRECT_URL = '/restaurants/'
#LOGIN_ERROR_URL    = '/login-error/' # need to make a login error and 404 pages

# Google AUTH Completion urls
#SOCIAL_AUTH_COMPLETE_URL_NAME  = 'socialauth_complete'
#SOCIAL_AUTH_ASSOCIATE_URL_NAME = 'socialauth_associate_complete'

# Social Auth URLS
#SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/home/'
#SOCIAL_AUTH_LOGIN_URL = '/'


################## Ajax Selects Settings for Auto-Complete #############

# define the lookup channels in use on the site
AJAX_LOOKUP_CHANNELS = {
    #  simple: search Person.objects.filter(name__icontains=q)
   # 'person'  : {'model': 'example.person', 'search_field': 'name'},
    # define a custom lookup channel
   # 'song'   : ('example.lookups', 'SongLookup')
}


ROOT_URLCONF = 'meHungry_project.urls'

WSGI_APPLICATION = 'meHungry_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# Parse database configuration from $DATABASE_URL
#import dj_database_url
#DATABASES = {'default': dj_database_url.config(default='postgres://localhost')}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mehungry',
        'USER': 'pranaykumar',
        'PASSWORD': '',
       # 'HOST': '54.148.25.160',
       # 'PORT': '3306',
    }
}

#CARTON Settings
CART_PRODUCT_MODEL='meHungry_customer_website.models.FoodItem'

CART_TEMPLATE_TAG_NAME = 'get_cart'

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = ''

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    BASE_DIR + '/templates',
    BASE_DIR + '/media',
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)
# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)



TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



# Custom user
AUTH_USER_MODEL = 'meHungry_customer_website.MyUser'
