import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-change-me-in-production')

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',  # Required for django-esi and some auth features

    # Third Party Apps
    'esi',                  # Django-ESI: The core EVE integration
    'channels',             # ASGI/Websockets support
    'django_eventstream',   # Server-Sent Events for real-time updates
    'django_celery_results',# Store task results in DB
    'django_celery_beat',   # Periodic tasks (e.g., updating SDE nightly)
    
    # Local Apps (Your Custom Apps)
    'core',
    'eve_auth',             # Alt management & SSO extension
    'sde',                  # Static Data Export management
    'fleets',               # Waitlist & Fleet logic
    'integrations',         # Centralized ESI calls
]

SITE_ID = 1  # Required for django.contrib.sites

MIDDLEWARE = [
    'django_grip.GripMiddleware',  # Required for django-eventstream
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'], # Pointing to the global templates folder
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

# WSGI for standard requests, ASGI for Async/Real-time
WSGI_APPLICATION = 'config.wsgi.application'
ASGI_APPLICATION = 'config.asgi.application' 


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'eve_fleet_db'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC' # EVE Online runs on UTC (EVE Time), keep this UTC!
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ==============================================================================
# EVE ONLINE / DJANGO-ESI CONFIGURATION
# ==============================================================================

# Get these from https://developers.eveonline.com/
ESI_SSO_CLIENT_ID = os.environ.get('ESI_CLIENT_ID', '')
ESI_SSO_CLIENT_SECRET = os.environ.get('ESI_CLIENT_SECRET', '')
ESI_SSO_CALLBACK_URL = os.environ.get('ESI_CALLBACK_URL', 'http://localhost:8000/sso/callback')

# MANDATORY: Developer contact email for CCP (User-Agent header)
ESI_USER_CONTACT_EMAIL = os.environ.get('ESI_USER_CONTACT_EMAIL', 'your-email@example.com')

# Scopes required for your app (Add more as features require)
ESI_SSO_SCOPES = [
    'publicData',
    'esi-fittings.read_fittings.v1',
    'esi-location.read_ship_type.v1',
    'esi-skills.read_skills.v1',
    'esi-clones.read_implants.v1',
]


# ==============================================================================
# CELERY CONFIGURATION (Async Tasks)
# ==============================================================================

CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
CELERY_RESULT_BACKEND = 'django-db' # Store results in django_celery_results
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE


# ==============================================================================
# CHANNELS & EVENTSTREAM (Real-time)
# ==============================================================================

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_HOST', 'localhost'), 6379)],
        },
    },
}

# Allow EventStream from all hosts for now (lock down in production)
EVENTSTREAM_ALLOW_ORIGIN = '*'
EVENTSTREAM_STORAGE_CLASS = 'django_eventstream.storage.DjangoModelStorage'