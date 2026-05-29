from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import RegisterView, me_view, avatar_upload_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', TokenObtainPairView.as_view(), name='api-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='api-token-refresh'),
    path('me/', me_view, name='api-me'),
    path('avatar/', avatar_upload_view, name='api-avatar-upload'),
]
