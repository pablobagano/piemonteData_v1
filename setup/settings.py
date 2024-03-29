"""
Django settings for setup project.

Generated by 'django-admin startproject' using Django 4.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
import pymysql
from django.db import DatabaseError, connections
from django.contrib.messages import constants as messages
from azure.storage.blob import BlobClient
import tempfile 
import logging 

pymysql.install_as_MySQLdb()
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False') == 'True'
if DEBUG:
    print('Debugging')

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split()

CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS').split()

# Security Settings
SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'False') == 'True'
if os.getenv('USE_SECURE_PROXY_SSL_HEADER', 'False') == 'True':
    SECURE_PROXY_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'False') == 'True'
_csrf_trusted_origings = os.getenv('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = _csrf_trusted_origings.split(',') if _csrf_trusted_origings else []

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    'storages',
    'corsheaders',
    'piemonteStructure.apps.PiemontestructureConfig'
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware"
]

ROOT_URLCONF = "setup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "setup.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
if DEBUG:
    print("SQLite DB")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    try:
        conn_string = os.getenv('CONN_STRING')
        blob_url = os.getenv('BLOB_URL')
        blob_client = BlobClient.from_connection_string(
            conn_string, 
            container_name=os.getenv('CONTAINER_NAME'),
            blob_name= os.getenv('BLOB_NAME')
        )
        blob_stream = blob_client.download_blob()
        blob_data = blob_stream.readall()
    except Exception as e:
        logger = logging.getLogger(__name__)
        logger.exception(f"{e}")
        print(f"{type(e)}: {e.__name__}")
    try:
        temp_cert_file = tempfile.NamedTemporaryFile(delete=False)
        temp_cert_file.write(blob_data)
        temp_cert_path = temp_cert_file.name
        temp_cert_file.close()
        print(f"Blob data successfully fetched and written to {temp_cert_path}")
    except Exception as e:
        print(f"{type(e)}: {e}")

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/


if DEBUG:
    STATIC_URL = "static/"
else:
    AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
    AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
    AZURE_CONTAINER = os.getenv('AZURE_CONTAINER')
    STATICFILES_STORAGE = "storages.backends.azure_storage.AzureStorage"
    AZURE_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
    STATIC_URL = f"https://{AZURE_DOMAIN}/{AZURE_CONTAINER}/"

STATICFILES_DIR = [
    os.path.join(BASE_DIR, 'setup/static')
]



# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email Settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 465))
EMAIL_USE_SSL = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

if not EMAIL_HOST_USER:
    raise ValueError("EMAIL_HOST_USER must be set in environment")
if not EMAIL_HOST_PASSWORD:
    raise ValueError("EMAIL_HOST_PASSWORD must be set in environment")

# BASE_URL

BASE_URL = os.getenv('BASE_URL', 'http:localhost:8000')

# LOGIN_URL

LOGIN_URL = '/login/'