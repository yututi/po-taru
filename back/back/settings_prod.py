
from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [os.environ.get('VIRTUAL_HOST')]

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# DB使わないので初期値
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# dockerのvolumeを指定
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
