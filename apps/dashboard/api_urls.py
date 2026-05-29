from django.urls import path
from .api_views import stats_view, recent_view

urlpatterns = [
    path('stats/', stats_view, name='api-dashboard-stats'),
    path('recent/', recent_view, name='api-dashboard-recent'),
]
