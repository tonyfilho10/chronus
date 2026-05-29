from django.contrib import admin
from .models import TutorialCategory, Tutorial


@admin.register(TutorialCategory)
class TutorialCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order',)


@admin.register(Tutorial)
class TutorialAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'difficulty', 'estimated_minutes', 'is_published', 'order')
    list_filter = ('category', 'difficulty', 'is_published')
    list_editable = ('is_published', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'description', 'content')
    ordering = ('category__order', 'order')
