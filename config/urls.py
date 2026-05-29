from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

urlpatterns = [
    path("admin/", admin.site.urls),

    # Auth (allauth)
    path("accounts/", include("allauth.urls")),

    # API
    path("api/auth/", include("apps.accounts.api_urls")),
    path("api/prompts/", include("apps.prompts.api_urls")),
    path("api/dashboard/", include("apps.dashboard.api_urls")),
    path("api/community/", include("apps.community.api_urls")),
    path("api/templates/", include("apps.templates_library.api_urls")),
    path("api/exports/", include("apps.exports.api_urls")),

    # OpenAPI docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

    # Frontend views
    path("", include("apps.prompts.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("community/", include("apps.community.urls")),
    path("templates/", include("apps.templates_library.urls")),
    path("settings/", include("apps.accounts.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
