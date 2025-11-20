from .settings import *   # Load all base settings
from decouple import config

# ENV / DEBUG
DEBUG = config('DEBUG', default=False, cast=bool)

# Static files storage (Azure / Production)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

_allowed = config('ALLOWED_HOSTS', default='')
ALLOWED_HOSTS = [h.strip() for h in _allowed.split(',') if h.strip()]

if config('ALLOW_LOCALHOST', default='0') in ('1', 'true', 'True'):
    ALLOWED_HOSTS += ['127.0.0.1', 'localhost']

# Ensure Oryx internal host present (safe default)
if config('INCLUDE_AZURE_INTERNAL_HOST', default='1') in ('1', 'true', 'True'):
    if '169.254.130.2' not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append('169.254.130.2')

# CSRF Trusted Origins: ensure https scheme for domains
CSRF_TRUSTED_ORIGINS = []
for h in ALLOWED_HOSTS:
    if h.startswith('http://') or h.startswith('https://'):
        CSRF_TRUSTED_ORIGINS.append(h)
    else:
        CSRF_TRUSTED_ORIGINS.append('https://' + h)



# Database with sanitized sslmode
DB_SSLMODE = config('DB_SSLMODE', default='disable')  # env must be one of disable|allow|prefer|require|verify-ca|verify-full
if DB_SSLMODE not in ('disable','allow','prefer','require','verify-ca','verify-full'):
    DB_SSLMODE = 'require'

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
