from rest_framework import serializers
from .models import PromptTemplate


class PromptTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptTemplate
        fields = ('id', 'name', 'description', 'category', 'stack_target', 'is_official', 'use_count', 'created_at')
