
from datetime import timedelta
import datetime
from enum import nonmember
import os
from pathlib import Path
from re import L
from socket import if_indextoname
from decouple import config
import colorlog


import logging
logging.basicConfig(level=logging.DEBUG)




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent





SECRET_KEY = config('DJANGO_SERVER')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]



# # Application definition
# from firebase_admin import credentials, firestore, initialize_app

# # Use a service account
# cred = credentials.Certificate('myapp/models_folder/serviceAccount.json')
# initialize_app(cred)

# db = firestore.client()



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'myapp',
    'myapp.configurations',
    
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt.token_blacklist',
    'drf_yasg',
    'channels',
    'sentry_sdk',
    'sentry_sdk.integrations.django',
    'db_email_backend',  
    "debug_toolbar",
        'django_extensions',

]


SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'basic': {
            'type': 'basic'
        }
        
        

    },
    'USE_SESSION_AUTH': False,
    
}

# settings.py






EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST")
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER =config("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD")

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (


        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}




SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    


    'ALGORITHM': 'HS512',
    'VERIFYING_KEY': None,

    'AUDIENCE': "Nir  Fullstack Project",    
    'ISSUER': "None",
    'JWK_URL': None, # not used because we are using the Hs512 Algorithm
    'LEEWAY': 120, # sec
    
    



    'AUTH_HEADER_TYPES': ('Bearer',),
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
    'corsheaders.middleware.CorsMiddleware',  # This should be first
    'debug_toolbar.middleware.DebugToolbarMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
ROOT_URLCONF = 'project.urls'


import sentry_sdk 
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.crons.decorator import monitor
from decouple import config,AutoConfig


# Create an instance of the AutoConfig class
config = AutoConfig()
SENTRY_DSN = config('SENTRY_DSN')

# Initialize the Sentry SDK with the Django integration and the DSN value from the .env file    
sentry_sdk.init(
    dsn=SENTRY_DSN, # type: ignore
    integrations=[DjangoIntegration()]
    
)
@monitor(monitor_slug='my-cron-monitor')
def tell_the_world(msg):
    print(msg)

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
ASGI_APPLICATION = 'myproject.routing.application'  # new for channels (websockets and more  )

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite',
    }}


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

TIME_ZONE = 'UTC'

USE_I18N = True


USE_TZ = True



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static/')

# Media files (Uploaded by users)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField' 

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3001',
    'http://10.0.0.9:3001',
    "http://localhost:3000",
    "http://127.0.0.1:3000",  
    "http://192.168.0.253:3000",
    "http://localhost:3000",
    "http://localhost:3002",
    
    "http://10.0.0.9:3002",
    "http://localhost:8081",
       "http://localhost:8082",
       "http://localhost:8083",
       "exp://10.0.0.11:8082",
       "exp://10.0.0.11:8083",
       "http://192.168.1.123:8083",
       "http://192.168.1.123:8082",
       'http://localhost:4200',
         'http://localhost:4201',

    
        


]# Import necessary module
from termcolor import colored
import os

from colorlog import ColoredFormatter

class StatusCodeFormatter(ColoredFormatter):
    def format(self, record):
        # קריאה לשיטת הפורמט של המחלקה האב
        log_msg = super().format(record)

        # בדיקה אם קוד הסטטוס נמצא בהודעת הלוג
        if 'status_code' in record.__dict__:
            status_code = record.status_code  # type: ignore

            # צביעת קוד הסטטוס בהתאם לערכו
            if status_code in range(199, 301):
                # מוצלח - ירוק עם רקע לבן
                log_msg = log_msg.replace(str(status_code), "\033[32;47m{}\033[0m".format(status_code))
            elif status_code in range(300, 401):
                # פחות מוצלח - צהוב עם רקע לבן
                log_msg = log_msg.replace(str(status_code), "\033[33;47m{}\033[0m".format(status_code))
            elif status_code in range(400, 501):
                # לא ממש מצליח - כחול עם רקע לבן
                log_msg = log_msg.replace(str(status_code), "\033[34;47m{}\033[0m".format(status_code))
            elif status_code in range(500, 601):
                # לא מצליח - אדום עם רקע לבן
                log_msg = log_msg.replace(str(status_code), "\033[31;47m{}\033[0m".format(status_code))

        return log_msg

# Define the logging configuration
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
            '()':  StatusCodeFormatter,  # Use the custom StatusCodeFormatter
            'format': "%(log_color)s%(levelname)-8s%(reset)s %(blue)s%(asctime)s%(reset)s %(log_color)s%(message)s%(reset)s %(cyan)sfrom %(module)s, line %(lineno)d in %(funcName)s%(reset)s",
            'datefmt': "%Y-%m-%d %H:%M:%S",
            'log_colors': {
                'DEBUG': 'blue',
                'INFO': 'green',
                'WARNING': 'red.bg_yellow',
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
