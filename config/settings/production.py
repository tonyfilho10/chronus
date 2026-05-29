from .base import *  # noqa
from decouple import config

# ── ALLOWED_HOSTS ──────────────────────────────────────────
# Inclui Railway (healthcheck + subdominios) + dominio customizado via env
_extra_hosts = config("ALLOWED_HOSTS", default="")
ALLOWED_HOSTS = [
    ".railway.app",       # todos os subdominios Railway (healthcheck, web, etc.)
    "healthcheck.railway.app",
    "localhost",
    "127.0.0.1",
] + [h.strip() for h in _extra_hosts.split(",") if h.strip()]

# ── Segurança ──────────────────────────────────────────────
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Desabilita redirect HTTPS para o healthcheck do Railway funcionar via HTTP
SECURE_SSL_REDIRECT = False

# ── CORS ───────────────────────────────────────────────────
_origins = config("CORS_ALLOWED_ORIGINS", default="")
CORS_ALLOWED_ORIGINS = [s.strip() for s in _origins.split(",") if s.strip()]
if not CORS_ALLOWED_ORIGINS:
    CORS_ALLOW_ALL_ORIGINS = True

# ── Cache (sem Redis por padrão — usa memória local) ───────
REDIS_URL = config("REDIS_URL", default="")
if REDIS_URL:
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL,
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"
else:
    CACHES = {"default": {"BACKEND": "django.core.cache.backends.locmem.LocMemCache"}}
    SESSION_ENGINE = "django.contrib.sessions.backends.db"

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
    },
}

# ── Sentry (opcional) ──────────────────────────────────────
_sentry_dsn = config("SENTRY_DSN", default="")
if _sentry_dsn:
    import sentry_sdk
    sentry_sdk.init(dsn=_sentry_dsn, traces_sample_rate=0.05, environment="production")
