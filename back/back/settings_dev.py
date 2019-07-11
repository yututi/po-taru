
from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# accept the access from webpack-dev-server.
ALLOWED_HOSTS = ["*"]
INSTALLED_APPS.append('corsheaders')
MIDDLEWARE.append('corsheaders.middleware.CorsMiddleware')
CORS_ORIGIN_ALLOW_ALL = True

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# disable csrf validation in debug.
# MIDDLEWARE.append('back.middlewares.DisableCSRFMiddleware')