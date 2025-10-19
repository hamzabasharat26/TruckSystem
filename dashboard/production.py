from .settings import *
import os
import dj_database_url

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['.azurewebsites.net', 'localhost', '127.0.0.1']

# Database configuration
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Use WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Remove channels for Azure compatibility
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'channels']
ASGI_APPLICATION = None

# Simplified detection for Azure
DETECTION_DATA_DIR = BASE_DIR / 'detection_data'
JSON_DETECTIONS_DIR = DETECTION_DATA_DIR / 'json_detections'

# Create directories if they don't exist
os.makedirs(JSON_DETECTIONS_DIR, exist_ok=True)

# Disable real-time detection processor for Azure
def start_detection_processor():
    print("⚠️ Detection processor disabled for Azure deployment")

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}