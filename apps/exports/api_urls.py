from django.urls import path
from .api_views import export_view

urlpatterns = [
    path('<uuid:pk>/', export_view, name='api-export'),
]
