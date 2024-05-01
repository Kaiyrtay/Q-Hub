"""
Qualification Hub Project Overview

Qualification Hub is a Django-based project designed to manage and track 
educational qualifications, certificates, and related information. It 
supports various roles, including teachers, students, managers, and others, 
allowing them to manage their certificates and track their qualifications.

Key Components:
- **Models**: Defines entities like `Certificate`, `Teacher`, `Student`, `Manager`, 
  `Department`, and `Faculty`.
- **Views**: Manages interactions with the models, including class-based views for 
  listing, creating, updating, and deleting records.
- **Mixins**: Provides mixins for handling permissions and access control, ensuring 
  appropriate users have access to specific functionalities.
- **Search Functionality**: Implements search logic across various models to allow 
  users to search for certificates, users, departments, etc.
- **Authentication and Authorization**: Handles user authentication (login, logout, 
  registration) and authorization with different permission levels and groups.

Roles and Permissions:
- **Owner**: A superuser with full access to the project.
- **Admin**: A staff member with access to managers, departments, and faculties.
- **Manager**: A manager with access to teachers and students.
- **Teacher**: A teacher with access to certificates.
- **Student**: A student with access to certificates.
- **Guest**: A non-authenticated user with read-only access to public information.

Dependencies:
- Utilizes Django for the core framework, including `django.contrib.auth.models` 
  for user and group management.
- Employs `crispy_forms` for enhanced form handling and layout customization.
- Interacts with various models and Django features like permissions and content types.

Author: [Your Name]
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # local apps
    'faculties',
    'departments',
    'managers',
    'teachers',
    'students',
    'certificates',
    'core',
    # third party apps
    "crispy_forms",
    'bootstrap5',
    "crispy_bootstrap5",
    # third party apps to translate page
    'rosetta',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # Needed for language switching
    'whitenoise.middleware.WhiteNoiseMiddleware',  # WhiteNoise
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # local
    'core.middleware.StaffOnlyMiddleware'
]

ROOT_URLCONF = 'qualification_hub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'qualification_hub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

# settings.py

LANGUAGE_CODE = 'en-us'  # Default language
USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True  # Enable timezone support

LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('kk', _('Kazakh')),
]
LOCALE_PATHS = [
    BASE_DIR / 'locale/',
]

ROSETTA_ACCESS_CONTROL_FUNCTION = 'django.contrib.auth.decorators.login_required'

TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# This is the URL to access static files in the browser
STATIC_URL = '/static/'

# This is the directory where static files are collected from your apps
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# This tells Django where to look for additional static files during development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Allows Django's static files finders to work with WhiteNoise
WHITENOISE_USE_FINDERS = True
# Disable autorefresh in production for better performance
WHITENOISE_AUTOREFRESH = False

# Crispy form
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = 'core:login'
LOGOUT_URL = 'core:logout'

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',  # Default authentication
]

# Email backend that sends emails to the console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
