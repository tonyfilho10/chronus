from django.urls import path
from .api_views import TemplateListView

urlpatterns = [
    path('', TemplateListView.as_view(), name='api-templates'),
]
