import os

DEBUG = True

# Path of our project:
BASE_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), os.pardir))

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
ALLOWED_HOSTS = []

TIME_ZONE = 'Europe/Oslo'
LANGUAGE_CODE = 'nb'
USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'asdf123'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'bestilling.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'bestilling.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'rest_framework',
)
INSTALLED_APPS += (
    'design',
    'tekst',
    'prm',
    'bestilling'
)

SITE_ID = 1

# Trello keys, tokens and board ids
TRELLO_API_KEY = ""
TRELLO_TOKEN = ""
TRELLO_DESIGN_BOARD_ID = ""
TRELLO_TEKST_BOARD_ID = ""
TRELLO_PRM_BOARD_ID = ""

MAIL_KAK_DESIGN = 'kak-design@studentersamfundet.no'
MAIL_KAK_TEKST = 'kak-tekst@studentersamfundet.no'
MAIL_KAK_PRM = 'kak-prm@studentersamfundet.no'

UPLOAD_FILENAME_EXTENSIONS_ALLOWED = [
    'png', 'ai', 'eps', 'jpeg', 'jpg', 'tif', 'tiff', 'indd', 'webp'
    'pdf', 'doc', 'docx', 'xls', 'xlsx', 'txt', 'zip', '.gif']

try:
    from .local_settings import *
except ImportError:
    pass
