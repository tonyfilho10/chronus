import pytest
from django.utils import timezone
from unittest.mock import patch, MagicMock


@pytest.mark.django_db
class TestAccountService:
    def test_has_quota_within_limit(self, user_factory):
        from apps.accounts.services import AccountService
        user = user_factory(monthly_quota=10)
        assert AccountService.has_quota(user) is True

    def test_has_quota_exceeded(self, user_factory):
        from apps.accounts.services import AccountService
        from apps.accounts.models import UsageCounter
        user = user_factory(monthly_quota=2)
        today = timezone.now().date().replace(day=1)
        UsageCounter.objects.create(user=user, month=today, generation_count=2)
        assert AccountService.has_quota(user) is False

    def test_increment_usage(self, user_factory):
        from apps.accounts.services import AccountService
        from apps.accounts.models import UsageCounter
        user = user_factory()
        AccountService.increment_usage(user, tokens=500)
        today = timezone.now().date().replace(day=1)
        counter = UsageCounter.objects.get(user=user, month=today)
        assert counter.generation_count == 1
        assert counter.tokens_consumed == 500

    def test_log_action_creates_audit_log(self, user_factory):
        from apps.accounts.services import AccountService
        from apps.accounts.models import AuditLog
        user = user_factory()
        AccountService.log_action(user, "test_action", "Prompt", metadata={"key": "value"})
        log = AuditLog.objects.get(user=user, action="test_action")
        assert log.resource_type == "Prompt"
        assert log.metadata == {"key": "value"}
