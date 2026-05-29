from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.prompts.models import Prompt
from apps.community.models import Upvote


@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def upvote_view(request, pk):
    try:
        prompt = Prompt.objects.get(pk=pk, is_public=True)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt não encontrado.'}, status=404)

    if request.method == 'POST':
        Upvote.objects.get_or_create(user=request.user, prompt=prompt)
        return Response({'upvoted': True})
    else:
        Upvote.objects.filter(user=request.user, prompt=prompt).delete()
        return Response({'upvoted': False})
