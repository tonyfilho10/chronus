from .base import *  # noqa

DEBUG = True

CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# SQLite para dev local sem Supabase
from decouple import config as _cfg
_db_host = _cfg("DB_HOST", default="localhost")
if _db_host in ("localhost", "127.0.0.1", ""):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",  # noqa
        }
    }
else:
    DATABASES["default"]["OPTIONS"]["sslmode"] = "disable"  # noqa

# Cache e sessão sem Redis em dev local
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.db"

# Celery em modo síncrono para dev
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# CSP relaxada em dev: permite Alpine.js (unsafe-eval) e Tailwind browser build
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'", "'unsafe-eval'", "'unsafe-inline'", "unpkg.com", "cdn.jsdelivr.net"),
        "style-src": ("'self'", "'unsafe-inline'", "fonts.googleapis.com", "cdn.jsdelivr.net"),
        "font-src": ("'self'", "fonts.gstatic.com"),
        "img-src": ("'self'", "data:", "lh3.googleusercontent.com"),
        "connect-src": ("'self'",),
    }
}
