from django.urls import path
from .api_views import upvote_view

urlpatterns = [
    path('<uuid:pk>/upvote/', upvote_view, name='api-upvote'),
]
