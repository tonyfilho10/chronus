import json
import logging
from django.http import StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.accounts.permissions import IsOwner, IsEmailVerified
from .models import Prompt, RefinementSession
from .serializers import PromptSerializer, PromptListSerializer, GeneratePromptSerializer
from .services import PromptGenerationService, RefinementService, QuotaExceededError, LLMError, _META_PREFIX

logger = logging.getLogger("apps.prompts")


class PromptListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsEmailVerified]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["title", "idea_input"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return PromptListSerializer
        return PromptSerializer

    def get_queryset(self):
        return Prompt.objects.filter(
            user=self.request.user,
            status__in=[Prompt.Status.SAVED, Prompt.Status.ARCHIVED],
            deleted_at__isnull=True,
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PromptDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = PromptSerializer

    def get_queryset(self):
        return Prompt.objects.filter(user=self.request.user, deleted_at__isnull=True)

    def perform_destroy(self, instance):
        from django.utils import timezone
        instance.deleted_at = timezone.now()
        instance.status = Prompt.Status.DELETED
        instance.save(update_fields=["deleted_at", "status"])


def _sse_event(data: str, event: str = "message") -> str:
    lines = data.replace("\n", "\ndata: ")
    return f"event: {event}\ndata: {lines}\n\n"


@login_required
def generate_stream_view(request):
    """SSE endpoint: POST /api/prompts/generate/stream/"""
    if request.method != "POST":
        return StreamingHttpResponse(
            iter([_sse_event(json.dumps({"error": "Method not allowed"}), "error")]),
            content_type="text/event-stream",
            status=405,
        )

    try:
        body = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return StreamingHttpResponse(
            iter([_sse_event(json.dumps({"error": "JSON inválido"}), "error")]),
            content_type="text/event-stream",
            status=400,
        )

    idea = body.get("idea", "").strip()[:2000]
    if not idea:
        return StreamingHttpResponse(
            iter([_sse_event(json.dumps({"error": "Campo 'idea' obrigatório"}), "error")]),
            content_type="text/event-stream",
            status=400,
        )

    stack = body.get("stack", "Django")
    complexity = body.get("complexity", "complete")
    focus = body.get("focus", [])

    service = PromptGenerationService()

    def event_stream():
        try:
            for chunk in service.generate_stream(
                user=request.user,
                idea=idea,
                stack=stack,
                complexity=complexity,
                focus=focus,
            ):
                if chunk.startswith(_META_PREFIX):
                    # Chunk especial com metadados (prompt_id, tokens) — envia como evento JSON
                    meta_json = chunk[len(_META_PREFIX):]
                    yield _sse_event(meta_json, "meta")
                else:
                    yield _sse_event(chunk)
            yield _sse_event("{}", "done")
        except QuotaExceededError as exc:
            yield _sse_event(json.dumps({"error": str(exc), "code": "quota_exceeded"}), "error")
        except LLMError as exc:
            logger.error("LLM generation failed: %s", exc)
            yield _sse_event(json.dumps({"error": "Erro na geração. Tente novamente."}), "error")
        except Exception as exc:
            logger.exception("Unexpected error in generate_stream_view")
            yield _sse_event(json.dumps({"error": "Erro interno."}), "error")

    response = StreamingHttpResponse(event_stream(), content_type="text/event-stream")
    response["Cache-Control"] = "no-cache"
    response["X-Accel-Buffering"] = "no"
    return response


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsEmailVerified])
def refine_view(request, pk):
    try:
        prompt = Prompt.objects.get(pk=pk, user=request.user, deleted_at__isnull=True)
    except Prompt.DoesNotExist:
        return Response({"error": "Prompt não encontrado."}, status=404)

    message = request.data.get("message", "").strip()
    if not message:
        return Response({"error": "Mensagem obrigatória."}, status=400)

    from django.utils import timezone
    from datetime import timedelta

    session, _ = RefinementSession.objects.get_or_create(
        prompt=prompt,
        defaults={
            "messages": [{"role": "assistant", "content": prompt.generated_content}],
            "expires_at": timezone.now() + timedelta(hours=2),
        },
    )

    service = RefinementService()
    chunks = list(service.refine_stream(session, message))
    return Response({"response": "".join(chunks)})


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsOwner])
def publish_view(request, pk):
    try:
        prompt = Prompt.objects.get(pk=pk, user=request.user)
    except Prompt.DoesNotExist:
        return Response({"error": "Prompt não encontrado."}, status=404)

    prompt.is_public = not prompt.is_public
    prompt.save(update_fields=["is_public"])
    return Response({"is_public": prompt.is_public})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def duplicate_view(request, pk):
    try:
        original = Prompt.objects.get(pk=pk, user=request.user)
    except Prompt.DoesNotExist:
        return Response({"error": "Prompt não encontrado."}, status=404)

    duplicate = Prompt.objects.create(
        user=request.user,
        title=f"Cópia de {original.title}",
        idea_input=original.idea_input,
        stack_target=original.stack_target,
        complexity_level=original.complexity_level,
        focus_tags=original.focus_tags,
        generated_content=original.generated_content,
        status=Prompt.Status.SAVED,
        token_count=original.token_count,
    )
    return Response(PromptSerializer(duplicate).data, status=201)
