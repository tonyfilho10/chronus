import uuid
from django.db import models
from apps.accounts.models import User
from apps.prompts.models import Prompt


class Upvote(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="upvotes")
    prompt = models.ForeignKey(Prompt, on_delete=models.CASCADE, related_name="upvotes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "prompt")
        indexes = [models.Index(fields=["prompt"])]
        verbose_name = "Upvote"

    def __str__(self):
        return f"{self.user.email} → {self.prompt}"
