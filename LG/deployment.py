from .settings import *   # Load all base settings
from decouple import config

# ENV / DEBUG
DEBUG = config('DEBUG', default=False, cast=bool)

# Static files storage (Azure / Production)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Hosts
_allowed = config('ALLOWED_HOSTS', default='')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

if config('ALLOW_LOCALHOST', default='0') in ('1', 'true', 'True'):
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

# CSRF Trusted Origins
CSRF_TRUSTED_ORIGINS = [
    f"http://{h}" if not (h.startswith('http')) else h
    for h in ALLOWED_HOSTS
]

# SECRET KEY
SECRET_KEY = config('SECRET_KEY', default='unsafe-secret-key')

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME', default='inventory'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='root'),
        'HOST': config('DB_HOST', default='127.0.0.1'),
        'PORT': config('DB_PORT', default=5432, cast=int),
        'OPTIONS': {
            'sslmode': config('DB_SSLMODE', default='disable')
        }
    }
}

WSGI_APPLICATION = 'LG.wsgi.application'
ROOT_URLCONF = 'LG.urls'
