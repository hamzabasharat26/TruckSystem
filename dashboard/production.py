from .settings import *
import os

# Security settings
DEBUG = False
ALLOWED_HOSTS = ['*']  # Allow all hosts

# Database - Use SQLite with correct path
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Remove the static directory warning by updating STATICFILES_DIRS
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Use WhiteNoise for static files
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Remove channels (no WebSockets on Azure)
INSTALLED_APPS = [app for app in INSTALLED_APPS if app != 'channels']
ASGI_APPLICATION = None

# Use WSGI
WSGI_APPLICATION = 'dashboard.wsgi.application'

# Detection directories
DETECTION_DATA_DIR = os.path.join(BASE_DIR, 'detection_data')
JSON_DETECTIONS_DIR = os.path.join(DETECTION_DATA_DIR, 'json_detections')
os.makedirs(JSON_DETECTIONS_DIR, exist_ok=True)

# Remove the detection processor startup
def start_detection_processor():
    print("⚠️ Detection processor disabled for Azure")

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'https://*.azurewebsites.net',
]
