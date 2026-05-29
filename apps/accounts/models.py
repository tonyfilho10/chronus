import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from apps.core.models import TimeStampedModel


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    avatar_url = models.URLField(blank=True)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)

    @property
    def avatar_src(self):
        """Retorna a URL do avatar — imagem enviada ou URL externa."""
        if self.avatar:
            return self.avatar.url
        return self.avatar_url or ""
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Plan(models.TextChoices):
        FREE = "free", "Free"
        PRO = "pro", "Pro"
        TEAM = "team", "Team"

    plan = models.CharField(max_length=10, choices=Plan.choices, default=Plan.FREE)
    monthly_quota = models.PositiveIntegerField(default=10)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.email


class UsageCounter(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="usage_counters")
    month = models.DateField()
    generation_count = models.PositiveIntegerField(default=0)
    tokens_consumed = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user", "month")
        verbose_name = "Contador de Uso"

    def __str__(self):
        return f"{self.user.email} — {self.month}"


class AuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=100)
    resource_id = models.UUIDField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    metadata = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["action"]),
        ]
        verbose_name = "Log de Auditoria"

    def __str__(self):
        return f"{self.action} — {self.created_at}"
