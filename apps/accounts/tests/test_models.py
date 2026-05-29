import pytest


@pytest.mark.django_db
class TestUserModel:
    def test_user_str(self, user_factory):
        user = user_factory(email="test@chronus.app")
        assert str(user) == "test@chronus.app"

    def test_user_default_plan(self, user_factory):
        user = user_factory()
        assert user.plan == "free"

    def test_user_default_quota(self, user_factory):
        user = user_factory()
        assert user.monthly_quota == 10

    def test_user_uuid_pk(self, user_factory):
        user = user_factory()
        assert user.pk is not None
        assert len(str(user.pk)) == 36  # UUID format
