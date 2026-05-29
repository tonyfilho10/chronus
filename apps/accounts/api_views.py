import os
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.files.storage import default_storage
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserRegisterSerializer, UserProfileSerializer, UserUpdateSerializer
from .services import AccountService

ALLOWED_IMG_TYPES = {"image/jpeg", "image/png", "image/webp", "image/gif"}
MAX_AVATAR_SIZE = 5 * 1024 * 1024  # 5 MB


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        AccountService.send_verification_email(request, user)
        return Response(
            {"detail": "Conta criada. Verifique seu e-mail para ativar."},
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET", "PATCH"])
@permission_classes([IsAuthenticated])
def me_view(request):
    if request.method == "GET":
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)

    serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@login_required
@require_POST
def avatar_upload_view(request):
    """Faz upload do avatar do usuário e salva no storage."""
    file = request.FILES.get("avatar")

    if not file:
        return JsonResponse({"error": "Nenhum arquivo enviado."}, status=400)

    if file.content_type not in ALLOWED_IMG_TYPES:
        return JsonResponse({"error": "Tipo de arquivo não suportado. Use JPG, PNG, WebP ou GIF."}, status=400)

    if file.size > MAX_AVATAR_SIZE:
        return JsonResponse({"error": "Arquivo muito grande. Máximo 5 MB."}, status=400)

    user = request.user

    # Remove avatar anterior se existir
    if user.avatar:
        try:
            default_storage.delete(user.avatar.name)
        except Exception:
            pass

    # Salva o novo avatar com nome baseado no user ID
    ext = os.path.splitext(file.name)[1].lower() or ".jpg"
    filename = f"avatars/{user.id}{ext}"
    saved_path = default_storage.save(filename, file)
    user.avatar.name = saved_path
    user.save(update_fields=["avatar"])

    return JsonResponse({
        "avatar_url": user.avatar.url,
        "message": "Avatar atualizado com sucesso!"
    })
