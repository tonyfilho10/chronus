import os
from .base import *  # noqa
from decouple import config

# ── Proxy (Railway usa HTTPS no edge, HTTP internamente) ───
USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ── ALLOWED_HOSTS ──────────────────────────────────────────
_extra_hosts = config("ALLOWED_HOSTS", default="")
ALLOWED_HOSTS = [
    ".railway.app",
    "healthcheck.railway.app",
    "localhost",
    "127.0.0.1",
] + [h.strip() for h in _extra_hosts.split(",") if h.strip() and h.strip() not in (".", "")]

# ── CSRF ───────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    "https://*.railway.app",
    "https://*.up.railway.app",
] + [
    f"https://{h.strip()}" for h in _extra_hosts.split(",")
    if h.strip() and not h.strip().startswith(".")
]

# ── Segurança ──────────────────────────────────────────────
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = False  # Railway gerencia HTTPS no edge
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ── Sessão: sempre banco de dados (sem depender de Redis) ──
SESSION_ENGINE = "django.contrib.sessions.backends.db"

# ── Cache: locmem por padrão, Redis se configurado ─────────
REDIS_URL = os.environ.get("REDIS_URL", "").strip()
if REDIS_URL and "localhost" not in REDIS_URL and "127.0.0.1" not in REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
else:
    CACHES = {
        "default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}
    }

# ── CORS ───────────────────────────────────────────────────
_origins = config("CORS_ALLOWED_ORIGINS", default="")
CORS_ALLOWED_ORIGINS = [s.strip() for s in _origins.split(",") if s.strip()]
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True

# ── Logs ───────────────────────────────────────────────────
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "{levelname} {asctime} {module} {message}", "style": "{"},
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "verbose"},
    },
    "root": {"handlers": ["console"], "level": "WARNING"},
    "loggers": {
        "apps": {"handlers": ["console"], "level": "INFO", "propagate": False},
        "django.security.DisallowedHost": {"handlers": [], "propagate": False},
        "django.request": {"handlers": ["console"], "level": "ERROR", "propagate": False},
    },
}

# ── Sentry (opcional) ──────────────────────────────────────
# ── CSP (permite Alpine.js + Tailwind browser) ─────────────
CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'", "'unsafe-eval'", "'unsafe-inline'", "unpkg.com", "cdn.jsdelivr.net"),
        "style-src": ("'self'", "'unsafe-inline'", "fonts.googleapis.com", "cdn.jsdelivr.net"),
        "font-src": ("'self'", "fonts.gstatic.com"),
        "img-src": ("'self'", "data:", "lh3.googleusercontent.com", "media"),
        "connect-src": ("'self'",),
    }
}

_sentry_dsn = config("SENTRY_DSN", default="")
if _sentry_dsn:
    import sentry_sdk
    sentry_sdk.init(dsn=_sentry_dsn, traces_sample_rate=0.05, environment="production")
