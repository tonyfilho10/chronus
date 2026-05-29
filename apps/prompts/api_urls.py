from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    PromptListCreateView, PromptDetailView,
    generate_stream_view, refine_view, publish_view, duplicate_view,
)

urlpatterns = [
    path('', PromptListCreateView.as_view(), name='api-prompt-list'),
    path('<uuid:pk>/', PromptDetailView.as_view(), name='api-prompt-detail'),
    path('generate/stream/', generate_stream_view, name='api-generate-stream'),
    path('<uuid:pk>/refine/', refine_view, name='api-prompt-refine'),
    path('<uuid:pk>/publish/', publish_view, name='api-prompt-publish'),
    path('<uuid:pk>/duplicate/', duplicate_view, name='api-prompt-duplicate'),
]
