import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = bool(os.environ.get("DEBUG", False))
ALLOWED_HOSTS = ["project.kpmtransport.no"]

if DEBUG:
    ALLOWED_HOSTS.extend(["0.0.0.0", "127.0.0.1"]) # windows

INSTALLED_APPS = []

MIDDLEWARE = []

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
    },
]

WSGI_APPLICATION = 'project.wsgi.application'
