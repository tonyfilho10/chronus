from django.contrib.auth import get_user_model


def site_context(request):
    """Injeta variáveis globais em todos os templates."""
    User = get_user_model()
    try:
        user_count = User.objects.filter(is_active=True).count()
    except Exception:
        user_count = 0
    return {
        "user_count": user_count,
        "site_name": "CHRONUS",
        "org_name": "CSHUB",
    }
