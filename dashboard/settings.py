"""
Django settings for dashboard project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

from decouple import config

import dj_database_url


def path(*parts):
    return os.path.join(BASE_DIR, *parts)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='secret-key-for-dev-only')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DJANGO_DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = ['*']

ROOT_URLCONF = 'dashboard.urls'

HEALTHCHECK_URL = '^%s$' % config('HEALTHCHECK_URL', default='__heartbeat__'),
LBHEALTHCHECK_URL = '^%s$' % config(
    'LBHEALTHCHECK_URL', default='__lbheartbeat__'
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_REDIRECT_EXEMPT = [
    '^%s$' % HEALTHCHECK_URL,
    '^%s$' % LBHEALTHCHECK_URL,
]

if DEBUG is False:
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_SECONDS = 600
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    X_FRAME_OPTIONS = 'DENY'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'django_extensions',
    'pipeline',
    'rest_framework',
    'rest_framework_swagger',
    'waffle',

    'dashboard',
    'dashboard.socialaccount.providers.fxa',
    'domains',
    'push'
]

if DEBUG:
    try:
        import debug_toolbar
        assert debug_toolbar
        INSTALLED_APPS += [
            'debug_toolbar'
        ]
    except:
        pass

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'csp.middleware.CSPMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'waffle.middleware.WaffleMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [path('templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                'dashboard.context_processors.conf_settings'
            ],
        },
    },
]

WSGI_APPLICATION = 'dashboard.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default="postgres://postgres@localhost:5432/push_dev_dashboard",
        cast=dj_database_url.parse
    )
}

DATABASES['default']['CONN_MAX_AGE'] = 500

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en'
LOCALE_PATHS = [
    path('locale',),
]

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = path('staticfiles',)
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, 'static'),
    path('push', 'static'),
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

# django-pipeline
PIPELINE = {
    'DISABLE_WRAPPER': True,
    'STYLUS_ARGUMENTS': '--sourcemap '
                        '--use %s/node_modules/autoprefixer-stylus' % BASE_DIR,
    'COMPILERS': (
        'pipeline.compilers.stylus.StylusCompiler',
    ),
    'STYLESHEETS': {
        'dashboard': {
            'source_filenames': (
                # Global
                'styles/main.styl',
                'styles/elements.styl',
                'styles/forms.styl',
                'styles/navigation.styl',

                # Login page
                'styles/login.styl',

                # Push applicaton landing page
                'styles/landing.styl',

                # Push application listing page
                'styles/list.styl',

                # Push application details page
                'styles/details.styl',
            ),
            'output_filename': 'css/dashboard.css',
        },
    },
    'JAVASCRIPT': {
        'dashboard': {
            'source_filenames': (
                # Global
                'js/main.js',
                'js/analytics.js',
                'js/sign_in.js',

                # Push application validation page
                'js/validation.js',
            ),
            'output_filename': 'js/dashboard.js'
        }
    }
}

# django-allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
)

SOCIALACCOUNT_PROVIDERS = {
    'fxa': {
        'OAUTH_ENDPOINT': config(
            'FXA_OAUTH_ENDPOINT',
            'https://oauth-stable.dev.lcip.org/v1/'
        ),
        'PROFILE_ENDPOINT': config(
            'FXA_PROFILE_ENDPOINT',
            'https://stable.dev.lcip.org/profile/v1/profile'
        )
    }
}

ACCOUNT_EMAIL_VERIFICATION = config('ACCOUNT_EMAIL_VERIFICATION',
                                    default='none')
ACCOUNT_LOGOUT_ON_GET = True
LOGIN_REDIRECT_URL = 'home'

# djangorestframework
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated'
    ]
}

SITE_ID = 1

# TODO: Set real stage/prod AUTOPUSH_KEYS_ENDPOINT
PUSH_MESSAGES_API_ENDPOINT = config('PUSH_MESSAGES_API_ENDPOINT', None)
PUSH_MESSAGES_API_TIMEOUT = 3.05

# Google Analytics
GOOGLE_ANALYTICS_ACCOUNT = config('GOOGLE_ANALYTICS_ACCOUNT', None)

# django-csp
CSP_DEFAULT_SRC = ("'self'", 'p.datadoghq.com')
CSP_FONT_SRC = ('code.cdn.mozilla.net', 'maxcdn.bootstrapcdn.com')
CSP_SCRIPT_SRC = ("'self'", 'cdn.jsdelivr.net', 'ajax.googleapis.com',
                  'www.google-analytics.com')
CSP_STYLE_SRC = ("'self'", 'cdn.jsdelivr.net', 'code.cdn.mozilla.net',
                 'maxcdn.bootstrapcdn.com', 'www.google-analytics.com')

RAVEN_DSN = config('RAVEN_DSN', None)
if RAVEN_DSN:
    RAVEN_CONFIG = {
        'dsn': RAVEN_DSN,
    }
    INSTALLED_APPS += [
        'raven.contrib.django.raven_compat',
    ]
