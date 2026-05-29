import uuid
from django.db import models
from apps.core.models import TimeStampedModel


class TutorialCategory(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=10, default="📚")
    order = models.PositiveSmallIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Categoria de Tutorial"
        verbose_name_plural = "Categorias de Tutorial"

    def __str__(self):
        return self.name


class Tutorial(TimeStampedModel):
    class Difficulty(models.TextChoices):
        BEGINNER = "beginner", "Iniciante"
        INTERMEDIATE = "intermediate", "Intermediário"
        ADVANCED = "advanced", "Avançado"

    category = models.ForeignKey(TutorialCategory, on_delete=models.CASCADE, related_name="tutorials")
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    description = models.TextField()
    content = models.TextField(help_text="Conteúdo em Markdown")
    difficulty = models.CharField(max_length=20, choices=Difficulty.choices, default=Difficulty.BEGINNER)
    estimated_minutes = models.PositiveSmallIntegerField(default=10)
    order = models.PositiveSmallIntegerField(default=0)
    is_published = models.BooleanField(default=True)
    tags = models.JSONField(default=list)

    class Meta:
        ordering = ["category__order", "order", "title"]
        verbose_name = "Tutorial"

    def __str__(self):
        return self.title
