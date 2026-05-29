from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.utils import timezone
from apps.accounts.models import UsageCounter
from apps.prompts.models import Prompt


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def stats_view(request):
    user = request.user
    today = timezone.now().date().replace(day=1)
    counter, _ = UsageCounter.objects.get_or_create(user=user, month=today)
    saved = Prompt.objects.filter(user=user, status='saved', deleted_at__isnull=True).count()
    return Response({
        'generation_count': counter.generation_count,
        'monthly_quota': user.monthly_quota,
        'tokens_consumed': counter.tokens_consumed,
        'saved_count': saved,
        'plan': user.plan,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recent_view(request):
    from apps.prompts.serializers import PromptListSerializer
    prompts = Prompt.objects.filter(user=request.user, deleted_at__isnull=True).order_by('-created_at')[:5]
    return Response(PromptListSerializer(prompts, many=True).data)
