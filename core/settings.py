import os
from pathlib import Path
from import_export.formats.base_formats import XLSX, CSV

IMPORT_EXPORT_FORMATS = [CSV, XLSX]

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '$yprlksgsp$^b14v^*(=caqmyc=*r^3&tf+@eh5=rfuwple!29sas'

APPEND_SLASH = True
DEBUG = True
DJANGO_DEBUG = True

ALLOWED_HOSTS = ["*"]

# FIX Cross Origin Opener Policy Header has been Ignored
X_FRAME_OPTIONS = 'SAMEORIGIN'
SECURE_CROSS_ORIGIN_OPENER_POLICY = None

AUTHENTICATION_BACKENDS = [
    'home.authbe.SidamasLDAPBackend',
    'django.contrib.auth.backends.ModelBackend',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Extension
    # 'debug_toolbar',
    'rest_framework',
    'rest_framework.authtoken',
    # 'django_browser_reload',
    'django_filters',
    'rest_framework_datatables',
    'import_export',
    
    # Application
    'home',
    'accounts',
    'dashboard',
    'masters',
    'users',
    'literasi',
]

MIDDLEWARE = [
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_browser_reload.middleware.BrowserReloadMiddleware',
    # 'core.middleware.AddVersionToStaticMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
        'rest_framework_datatables.renderers.DatatablesRenderer',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'rest_framework_datatables.filters.DatatablesFilterBackend',
    ),
    'DEFAULT_PAGINATION_CLASS': None,
}

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "sikawan",
        "USER": "kawan",
        "PASSWORD": "password",
        "HOST": "iotekno.id",
        # "HOST": "127.0.0.1",
        "PORT": "5432",
        # Adminer : https://emr.iotekno.id/adminer.php?pgsql=iotekno.id&username=kawan&db=dayatif_kawan&ns=public
    },
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = "Asia/Jakarta"

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "home/static/"),
    os.path.join(BASE_DIR, "dashboard/static/"),
    os.path.join(BASE_DIR, "literasi/static/"),
    os.path.join(BASE_DIR, "masters/static/"),
    os.path.join(BASE_DIR, "users/static/"),
]

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

SESSION_COOKIE_NAME = 'bnn_kawasan_rawan'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Authentication configuration
LOGIN_REDIRECT_URL="/dashboard/"
LOGOUT_REDIRECT_URL="/accounts/logged_out/"

LOGIN_URL = "/accounts/login/"

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'kawasanrawan@gmail.com'
EMAIL_HOST_PASSWORD = 'yaeqegxhdnkeecsh'
DEFAULT_FROM_EMAIL = '<kawasanrawan@gmail.com>'

# INTERNAL_IPS = [
#     "127.0.0.1",
#     "103.210.54.17",
#     "103.210.54.17:8003",
#     "0.0.0.0",
#     "http://127.0.0.1",
#     "http://103.210.54.17",
#     "http://103.210.54.17:8003",
#     "http://0.0.0.0",
# ]

# ALLOWED_HOSTS = [
#     "127.0.0.1",
#     "103.210.54.17",
#     "103.210.54.17:8003",
#     "0.0.0.0",
# ]

# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.history.HistoryPanel',
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
#     'debug_toolbar.panels.profiling.ProfilingPanel',
# ]