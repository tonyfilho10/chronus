import uuid
from django.db import models
from apps.core.models import TimeStampedModel
from apps.accounts.models import User


class PromptTemplate(TimeStampedModel):
    class Category(models.TextChoices):
        CRM = "crm", "CRM"
        ERP = "erp", "ERP"
        SAAS = "saas", "SaaS"
        ECOMMERCE = "ecommerce", "E-commerce"
        BLOG = "blog", "Blog"
        API = "api", "API-only"
        MARKETPLACE = "marketplace", "Marketplace"
        OTHER = "other", "Outro"

    name = models.CharField(max_length=150)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=Category.choices, default=Category.OTHER)
    content = models.TextField()
    stack_target = models.CharField(max_length=100, default="Django")
    is_official = models.BooleanField(default=False)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="templates"
    )
    is_public = models.BooleanField(default=True)
    use_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["-is_official", "-use_count"]
        verbose_name = "Template"

    def __str__(self):
        return self.name
