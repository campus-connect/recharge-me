import os
from django.contrib.messages import constants as message_constants
import django_heroku
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://b86ba5e3a4c745cba7bc55f18f237612@sentry.io/1526898",
    integrations=[DjangoIntegration()]
)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG') == 'True' # Python does not parse environment variables to Python objects, it just gets them as strings. 

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # 3rd party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'phonenumber_field',
    'referrals.apps.ReferralsConfig',
    'avatar',
    'django_celery_beat',
    'notifications',
    'robots',
    'django.contrib.sitemaps',


    # local apps
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
]

ROOT_URLCONF = 'recharge.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
            ('django.template.loaders.cached.Loader', [
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',

            ]),
            ],
        },
    },
]

WSGI_APPLICATION = 'recharge.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DATABASE_NAME'),
        'USER': os.environ.get('DATABASE_USER'),
        'PASSWORD': os.environ.get('DATABASE_PASSWORD'),
        'HOST': os.environ.get('DATABASE_HOST'),
        'PORT': os.environ.get('DATABASE_PORT'),
    }
}


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

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

TIME_ZONE = 'Africa/Lagos'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

DEFAULT_FILE_STORAGE = 'storages.backends.dropbox.DropBoxStorage'

DROPBOX_OAUTH2_TOKEN = os.environ.get('DROP_BOX_KEY')
DROPBOX_ROOT_PATH = 'agapeer'
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'storages.backends.dropbox.DropBoxStorage'
# STATICFILES_STORAGE = 'static_compress.CompressedStaticFilesStorage'

# Custom User Model

AUTH_USER_MODEL = 'accounts.CustomUser'

SITE_ID = os.environ.get('SITE_ID', 1)

if DEBUG == False:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT') == 'True'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# allauth customization
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7

ACCOUNT_FORMS = {
'signup': 'accounts.forms.CustomSignupForm',
'login': 'accounts.forms.CustomLoginForm',
'reset_password': 'accounts.forms.CustomResetPasswordForm',
}

ACCOUNT_ADAPTER = 'accounts.adapter.AccountAdapter'
DJANGO_REFERRALS_DEFAULT_INPUT_VALUE = '40ed41dc-d291-4358-ae4e-d3c07c2d67dc' # The token to be used by
                                                                              # default. WARNING: Must be uuid4

DJANGO_REFERRALS_DEFAULT_URL = 'http://localhost:8000/'                       # Address for referral link
DJANGO_REFERRALS_PREFIX = ''  
PHONENUMBER_DEFAULT_REGION = 'NG'
PHONENUMBER_DB_FORMAT = 'E164'

# Email configurations
EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.environ.get("SENDGRID_API_KEY")
SENDGRID_SANDBOX_MODE_IN_DEBUG = os.environ.get("SENDGRID_SANDBOX_MODE_IN_DEBUG") == 'True'

# celery
CELERY_BROKER_URL = 'redis://localhost:6379'  
CELERY_RESULT_BACKEND = 'redis://localhost:6379'  
CELERY_ACCEPT_CONTENT = ['application/json']  
CELERY_RESULT_SERIALIZER = 'json'  
CELERY_TASK_SERIALIZER = 'json'
# https://docs.celeryproject.org/en/latest/userguide/configuration.html#std:setting-beat_scheduler
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Message framework
MESSAGE_LEVEL = message_constants.DEBUG

# django-htmlmin settings 
# https://github.com/cobrateam/django-htmlmin
HTML_MINIFY = True

# Robot.txt
ROBOTS_CACHE_TIMEOUT = 60*60*24

#Heroku
django_heroku.settings(locals())
#Heroku