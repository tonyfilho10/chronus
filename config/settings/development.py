from .base import *  # noqa

DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

DATABASES["default"]["OPTIONS"]["sslmode"] = "disable"  # noqa
