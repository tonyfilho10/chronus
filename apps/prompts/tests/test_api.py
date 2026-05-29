import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestPromptAPI:
    def setup_method(self):
        self.client = APIClient()

    def test_list_requires_auth(self):
        res = self.client.get("/api/prompts/")
        assert res.status_code == 401

    def test_list_returns_user_prompts(self, user_factory, prompt_factory):
        user = user_factory()
        other = user_factory(email="other@test.com")
        prompt_factory(user=user, status="saved")
        prompt_factory(user=other, status="saved")

        self.client.force_authenticate(user=user)
        res = self.client.get("/api/prompts/")
        assert res.status_code == 200
        assert res.data["count"] == 1

    def test_soft_delete(self, user_factory, prompt_factory):
        user = user_factory()
        prompt = prompt_factory(user=user, status="saved")
        self.client.force_authenticate(user=user)

        res = self.client.delete(f"/api/prompts/{prompt.id}/")
        assert res.status_code == 204

        prompt.refresh_from_db()
        assert prompt.deleted_at is not None

    def test_duplicate(self, user_factory, prompt_factory):
        user = user_factory()
        prompt = prompt_factory(user=user, status="saved", generated_content="content")
        self.client.force_authenticate(user=user)

        res = self.client.post(f"/api/prompts/{prompt.id}/duplicate/")
        assert res.status_code == 201
        assert res.data["title"].startswith("Cópia de")

    def test_other_user_cannot_access(self, user_factory, prompt_factory):
        owner = user_factory()
        other = user_factory(email="attacker@test.com")
        prompt = prompt_factory(user=owner, status="saved")

        self.client.force_authenticate(user=other)
        res = self.client.get(f"/api/prompts/{prompt.id}/")
        assert res.status_code in (403, 404)
