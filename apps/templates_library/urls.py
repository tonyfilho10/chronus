from django.urls import path
from . import views

urlpatterns = [
    path('', views.templates_view, name='templates'),
]
