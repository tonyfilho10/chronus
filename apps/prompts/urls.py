from django.urls import path
from . import views

urlpatterns = [
    path('', views.generate_view, name='generate'),
    path('generate/', views.generate_view, name='generate-explicit'),
    path('prompts/', views.prompt_list_view, name='prompt-list'),
    path('prompts/<uuid:pk>/', views.prompt_detail_view, name='prompt-detail'),
]
