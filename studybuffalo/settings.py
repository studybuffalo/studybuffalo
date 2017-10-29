"""
Django settings for studybuffalo project.
"""

import environ

# Set the Base Directory
BASE_DIR = environ.Path(__file__) - 2

# Connect to the .env file
env = environ.Env()
environ.Env.read_env(env_file=BASE_DIR.path('..', 'config').file('studybuffalo.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if env('DEBUG') == "True" else False

ALLOWED_HOSTS = env('SERVER_ADDRESS').split(" ")

# Site ID
SITE_ID = 1

# Application definition
INSTALLED_APPS = [
    # Add your apps here to enable them
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'aminoglycoside_calculator.apps.AminoglycosideCalculatorConfig',
    'drug_price_calculator.apps.DrugPriceCalculatorConfig',
    'log_manager.apps.LogManagerConfig',
    'play.apps.PlayConfig',
    'rdrhc_calendar.apps.RdrhcCalendarConfig',
    'read.apps.ReadConfig',
    'study.apps.StudyConfig',
    'updates.apps.UpdatesConfig',
    'vancomycin_calculator.apps.VancomycinCalculatorConfig',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# Error Log Settings
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'app_log_file': {
            'level': env('APP_LOG_LEVEL'),
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': env('APP_LOG_FILE'),
            'formatter': 'standard',
            'maxBytes': 1024*1024*15,
            'backupCount': 10,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['app_log_file',],
            'level': env('APP_LOG_LEVEL'),
        },
    }
}

# URL Settings
ROOT_URLCONF = 'studybuffalo.urls'

# Template Settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR("studybuffalo", "templates"),
            BASE_DIR("templates"),
        ],
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

WSGI_APPLICATION = 'studybuffalo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}


# Password validation & authentication
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGIN_REDIRECT_URL = "/"

# allauth Settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
SOCIALACCOUNT_PROVIDERS = {
    "facebook": {
        "AUTH_PARAMS": {"auth_type": "reauthenticate"},
        "METHOD": "oauth2",
        "SCOPE": ["email",],
    },
    "google": {
        "AUTH_PARAMS": {"access_type": "online"},
        "SCOPE": ["email",],
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATE_FORMAT = "%Y-%m-%d"

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"

# Email Server Settings
EMAIL_BACKEND = env('EMAIL_BACKEND')
DEFAULT_FROM_EMAIL = env('DEFAULT_FROM_EMAIL')
EMAIL_HOST = env('EMAIL_HOST')
EMAIL_HOST_USER = env('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True if env('EMAIL_USE_TLS') == "True" else False
EMAIL_PORT = env('EMAIL_PORT')

# Media settings for uploaded content
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR('media')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR('static')

STATICFILES_DIRS = [
    BASE_DIR('studybuffalo', 'static'),
    BASE_DIR('vancomycin_calculator', 'static'),
    BASE_DIR('drug_price_calculator', 'static'),
    BASE_DIR('log_manager', 'static'),
]

# SECURITY SETTINGS
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_SSL_REDIRECT = True if env('SECURE_SSL_REDIRECT') == "True" else False
SECURE_HSTS_SECONDS = env('SECURE_HSTS_SECONDS')
SECURE_HSTS_INCLUDE_SUBDOMAINS = True if env('SECURE_HSTS_INCLUDE_SUBDOMAINS') == "True" else False
SECURE_HSTS_PRELOAD = True if env('SECURE_HSTS_PRELOAD') == "True" else False
SECURE_SESSION_COOKIE = True if env('SECURE_SESSION_COOKIE') == "True" else False
CSRF_COOKIE_SECURE = True if env('CSRF_COOKIE_SECURE') == "True" else False
X_FRAME_OPTIONS: 'DENY'