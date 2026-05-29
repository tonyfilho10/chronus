from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.prompts.models import Prompt
from apps.accounts.models import UsageCounter


@login_required
def dashboard_view(request):
    user = request.user
    today = timezone.now().date().replace(day=1)
    counter, _ = UsageCounter.objects.get_or_create(user=user, month=today)

    quota_pct = min(100, int((counter.generation_count / max(user.monthly_quota, 1)) * 100))
    saved_count = Prompt.objects.filter(user=user, status='saved', deleted_at__isnull=True).count()
    collection_count = user.collections.count()
    tokens_k = round(counter.tokens_consumed / 1000, 1)

    recent_prompts = Prompt.objects.filter(
        user=user, deleted_at__isnull=True
    ).order_by('-created_at')[:5]

    return render(request, 'pages/dashboard.html', {
        'stats': {
            'month_count': counter.generation_count,
            'quota_pct': quota_pct,
            'saved_count': saved_count,
            'collection_count': collection_count,
            'tokens_k': tokens_k,
        },
        'recent_prompts': recent_prompts,
    })
