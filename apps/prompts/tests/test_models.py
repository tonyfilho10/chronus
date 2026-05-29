import pytest
from apps.prompts.models import Prompt


@pytest.mark.django_db
class TestPromptModel:
    def test_prompt_str_with_title(self, prompt_factory):
        prompt = prompt_factory(title="Meu CRM")
        assert str(prompt) == "Meu CRM"

    def test_prompt_str_without_title(self, prompt_factory):
        prompt = prompt_factory(title="")
        assert str(prompt).startswith("Prompt ")

    def test_prompt_default_status(self, prompt_factory):
        prompt = prompt_factory()
        assert prompt.status == Prompt.Status.DRAFT

    def test_soft_delete(self, prompt_factory):
        from django.utils import timezone
        prompt = prompt_factory()
        prompt.deleted_at = timezone.now()
        prompt.save()
        assert prompt.is_deleted is True

    def test_prompt_uuid_pk(self, prompt_factory):
        prompt = prompt_factory()
        assert len(str(prompt.pk)) == 36
