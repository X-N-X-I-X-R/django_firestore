from datetime import timedelta
from decouple import config
import os
from pathlib import Path
import logging
from colorlog import ColoredFormatter
from os import getenv
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.DEBUG)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)

# Custom user model
AUTH_USER_MODEL = 'myapp.User'

ALLOWED_HOSTS = ["*"]
# settings.py
# HOST_NAME = '127.0.0.1:8989'
CORS_ALLOW_CREDENTIALS = True






INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'corsheaders',
    'rest_framework',
    'django_filters',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'channels',
    "debug_toolbar",
    'django_extensions',
    'django_countries',
]

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}



# Email Configuration
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_PORT = config('EMAIL_PORT', cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
ADMIN_EMAIL = config('ADMIN_EMAIL')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS512',
    'VERIFYING_KEY': None,
    'AUDIENCE': "Nir Fullstack Project",    
    'ISSUER': "None",
    'JWK_URL': None, 
    'LEEWAY': 120, 
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'myapp.middleware.APIMiddleware',
    'myapp.middleware.SecurityLoggingMiddleware',
    'myapp.middleware.CSRFMiddleware',
]



ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'
ASGI_APPLICATION = 'myproject.routing.application'


CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(config('REDIS_HOST'), config('REDIS_PORT', cast=int))],
        },
    },
}




AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
TIME_ZONE = 'Asia/Jerusalem'  # או כל אזור זמן אחר שמתאים לך
USE_TZ = True
# USE_I18N = True
# USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'mediafiles')
MEDIA_URL = '/media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [

    
]

class StatusCodeFormatter(ColoredFormatter):
    def format(self, record):
        log_msg = super().format(record)
        if 'status_code' in record.__dict__:
            status_code = record.status_code  # type: ignore
            if status_code in range(199, 301):
                log_msg = log_msg.replace(str(status_code), "\033[32;47m{}\033[0m".format(status_code))
            elif status_code in range(300, 401):
                log_msg = log_msg.replace(str(status_code), "\033[33;47m{}\033[0m".format(status_code))
            elif status_code in range(400, 501):
                log_msg = log_msg.replace(str(status_code), "\033[34;47m{}\033[0m".format(status_code))
            elif status_code in range(500, 601):
                log_msg = log_msg.replace(str(status_code), "\033[31;47m{}\033[0m".format(status_code))
        return log_msg

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'colorlog.StreamHandler',
            'formatter': 'colored',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'debug.log',
            'formatter': 'detailed',
        },
    },
    'formatters': {
        'colored': {
            '()': StatusCodeFormatter,  
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(log_color)s%(message)s%(reset)s %(cyan)sfrom %(module)s, line %(lineno)d in %(funcName)s%(reset)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'log_colors': {
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'yellow',  # תיקון ערך צבע לא תקין
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            },
        },
        'detailed': {
            'format': "%(asctime)s %(levelname)-8s %(module)s, line %(lineno)d in %(funcName)s: %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
        },
    },
    'loggers': {
        'django': {
            
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'myapp': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },  
    },
}






## myproject.routing.application 
# daphne -b 0.0.0.0 -p 8099 myproject.asgi:application

# Security Settings
SECURE_SSL_REDIRECT = False if DEBUG else True
SESSION_COOKIE_SECURE = False if DEBUG else True
CSRF_COOKIE_SECURE = False if DEBUG else True
CSRF_TRUSTED_ORIGINS = ['http://localhost:8000', 'http://127.0.0.1:8000']
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript access to CSRF token
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Add CSRF exempt URLs
CSRF_EXEMPT_URLS = [
    '/api/v1/auth/register/',
    '/api/v1/auth/login/',
    '/api/v1/auth/token/',
    '/api/v1/auth/token/refresh/'
]



