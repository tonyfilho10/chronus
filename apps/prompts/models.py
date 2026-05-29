import uuid
from django.db import models
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from apps.core.models import SoftDeleteModel, TimeStampedModel
from apps.accounts.models import User


class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Prompt(SoftDeleteModel):
    class ComplexityLevel(models.TextChoices):
        MVP = "mvp", "MVP"
        COMPLETE = "complete", "Completo"
        ENTERPRISE = "enterprise", "Enterprise"

    class ComplexityScore(models.TextChoices):
        LOW = "low", "Baixa"
        MEDIUM = "medium", "Média"
        HIGH = "high", "Alta"
        CRITICAL = "critical", "Crítica"

    class Status(models.TextChoices):
        DRAFT = "draft", "Rascunho"
        SAVED = "saved", "Salvo"
        ARCHIVED = "archived", "Arquivado"
        DELETED = "deleted", "Deletado"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="prompts")
    title = models.CharField(max_length=255, blank=True)
    idea_input = models.TextField()
    stack_target = models.CharField(max_length=100, default="Django")
    complexity_level = models.CharField(
        max_length=20, choices=ComplexityLevel.choices, default=ComplexityLevel.COMPLETE
    )
    focus_tags = models.JSONField(default=list)
    generated_content = models.TextField(blank=True)
    complexity_score = models.CharField(max_length=10, choices=ComplexityScore.choices, blank=True)
    complexity_reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.DRAFT)
    is_public = models.BooleanField(default=False)
    token_count = models.PositiveIntegerField(default=0)
    tags = models.ManyToManyField(Tag, through="PromptTag", blank=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["created_at"]),
            GinIndex(fields=["search_vector"]),
        ]
        verbose_name = "Prompt"

    def __str__(self):
        return self.title or f"Prompt {self.id}"


class PromptSection(TimeStampedModel):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="sections")
    section_number = models.PositiveSmallIntegerField()
    section_title = models.CharField(max_length=100)
    content = models.TextField()
    order = models.PositiveSmallIntegerField()

    class Meta:
        ordering = ["order"]
        unique_together = ("prompt", "section_number")

    def __str__(self):
        return f"{self.prompt} — Seção {self.section_number}"


class PromptVersion(TimeStampedModel):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="versions")
    version_number = models.PositiveSmallIntegerField()
    content_snapshot = models.TextField()
    change_summary = models.TextField(blank=True)

    class Meta:
        ordering = ["-version_number"]
        unique_together = ("prompt", "version_number")

    def __str__(self):
        return f"{self.prompt} v{self.version_number}"


class RefinementSession(TimeStampedModel):
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="refinement_sessions")
    messages = models.JSONField(default=list)
    expires_at = models.DateTimeField()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Refinamento de {self.prompt}"


class PromptTag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("prompt", "tag")


class Collection(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collections")
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    prompts = models.ManyToManyField(Prompt, blank=True)

    class Meta:
        verbose_name = "Coleção"

    def __str__(self):
        return f"{self.user.email} — {self.name}"
