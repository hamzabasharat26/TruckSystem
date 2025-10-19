import os
from .settings import *

# Azure Database Configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', ''),
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', ''),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}

# Azure Storage for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Security settings for production
DEBUG = False
ALLOWED_HOSTS = ['.azurewebsites.net', 'your-app-name.azurewebsites.net']

# HTTPS settings
SECURE_SSL_REDISRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Redis for Channels (Azure Redis Cache)
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [(os.environ.get('REDIS_URL', 'redis://localhost:6379'))],
        },
    },
}

# Celery configuration for Azure
CELERY_BROKER_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379')
CELERY_RESULT_BACKEND = os.environ.get('REDIS_URL', 'redis://localhost:6379')