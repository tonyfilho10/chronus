import pytest
from django.contrib.auth import get_user_model

User = get_user_model()

_user_counter = 0


@pytest.fixture
def user_factory(db):
    def make(email=None, **kwargs):
        global _user_counter
        _user_counter += 1
        if email is None:
            email = f"user{_user_counter}@test.com"
        kwargs.setdefault("monthly_quota", 10)
        kwargs.setdefault("is_active", True)
        user = User.objects.create_user(
            username=email,
            email=email,
            password="testpass123",
            **kwargs,
        )
        return user
    return make


@pytest.fixture
def prompt_factory(db, user_factory):
    def make(user=None, **kwargs):
        from apps.prompts.models import Prompt
        if user is None:
            user = user_factory()
        kwargs.setdefault("idea_input", "A test app idea")
        kwargs.setdefault("stack_target", "Django")
        kwargs.setdefault("status", Prompt.Status.DRAFT)
        kwargs.setdefault("generated_content", "")
        return Prompt.objects.create(user=user, **kwargs)
    return make


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def auth_client(api_client, user_factory):
    user = user_factory()
    api_client.force_authenticate(user=user)
    return api_client, user
