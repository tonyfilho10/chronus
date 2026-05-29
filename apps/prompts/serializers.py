from rest_framework import serializers
from .models import Prompt, PromptSection, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")


class PromptSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromptSection
        fields = ("section_number", "section_title", "content", "order")


class PromptListSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    upvote_count = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = (
            "id", "title", "idea_input", "stack_target", "complexity_level",
            "complexity_score", "status", "is_public", "token_count",
            "tags", "upvote_count", "created_at", "updated_at",
        )

    def get_upvote_count(self, obj):
        return obj.upvotes.count()


class PromptSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    sections = PromptSectionSerializer(many=True, read_only=True)
    upvote_count = serializers.SerializerMethodField()

    class Meta:
        model = Prompt
        fields = (
            "id", "title", "idea_input", "stack_target", "complexity_level",
            "focus_tags", "generated_content", "complexity_score", "complexity_reason",
            "status", "is_public", "token_count", "tags", "sections",
            "upvote_count", "created_at", "updated_at",
        )
        read_only_fields = ("id", "generated_content", "token_count", "created_at", "updated_at")

    def get_upvote_count(self, obj):
        return obj.upvotes.count()


class GeneratePromptSerializer(serializers.Serializer):
    idea = serializers.CharField(max_length=2000)
    stack = serializers.CharField(max_length=100, default="Django")
    complexity = serializers.ChoiceField(
        choices=["mvp", "complete", "enterprise"], default="complete"
    )
    focus = serializers.ListField(
        child=serializers.CharField(max_length=50), max_length=5, default=list
    )
