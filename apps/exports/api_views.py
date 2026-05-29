from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from apps.prompts.models import Prompt
from apps.prompts.services import ExportService


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def export_view(request, pk):
    try:
        prompt = Prompt.objects.get(pk=pk, user=request.user, deleted_at__isnull=True)
    except Prompt.DoesNotExist:
        return Response({'error': 'Prompt nao encontrado.'}, status=404)

    fmt = request.data.get('format', 'md')

    if fmt == 'md':
        content = ExportService.to_markdown(prompt)
        response = HttpResponse(content, content_type='text/markdown')
        response['Content-Disposition'] = f'attachment; filename="prompt-{prompt.id}.md"'
        return response

    if fmt == 'txt':
        content = ExportService.to_txt(prompt)
        response = HttpResponse(content, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="prompt-{prompt.id}.txt"'
        return response

    if fmt == 'pdf':
        if prompt.user.plan == 'free':
            return Response({'error': 'PDF disponivel apenas no plano Pro.'}, status=403)
        pdf_bytes = ExportService.to_pdf(prompt)
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="prompt-{prompt.id}.pdf"'
        return response

    return Response({'error': 'Formato invalido. Use: md, txt ou pdf.'}, status=400)
