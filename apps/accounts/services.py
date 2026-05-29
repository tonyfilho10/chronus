import logging
from django.utils import timezone
from apps.accounts.models import UsageCounter, AuditLog

logger = logging.getLogger("apps.accounts")


class AccountService:
    @staticmethod
    def send_verification_email(request, user):
        from allauth.account.utils import send_email_confirmation
        try:
            send_email_confirmation(request, user)
        except Exception as exc:
            logger.error("Failed to send verification email: %s", exc)

    @staticmethod
    def get_or_create_usage_counter(user):
        today = timezone.now().date().replace(day=1)
        counter, _ = UsageCounter.objects.get_or_create(user=user, month=today)
        return counter

    @staticmethod
    def has_quota(user):
        counter = AccountService.get_or_create_usage_counter(user)
        return counter.generation_count < user.monthly_quota

    @staticmethod
    def increment_usage(user, tokens=0):
        counter = AccountService.get_or_create_usage_counter(user)
        counter.generation_count += 1
        counter.tokens_consumed += tokens
        counter.save(update_fields=["generation_count", "tokens_consumed"])

    @staticmethod
    def log_action(user, action, resource_type, resource_id=None, request=None, metadata=None):
        ip = None
        ua = ""
        if request:
            x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
            ip = x_forwarded.split(",")[0] if x_forwarded else request.META.get("REMOTE_ADDR")
            ua = request.META.get("HTTP_USER_AGENT", "")

        AuditLog.objects.create(
            user=user,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            ip_address=ip,
            user_agent=ua,
            metadata=metadata or {},
        )
