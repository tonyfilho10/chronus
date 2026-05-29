from django.urls import path
from . import views

urlpatterns = [
    path('', views.tutorial_list_view, name='tutorials'),
    path('<slug:slug>/', views.tutorial_detail_view, name='tutorial-detail'),
]
