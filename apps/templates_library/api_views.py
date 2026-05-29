from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import PromptTemplate
from .serializers import PromptTemplateSerializer


class TemplateListView(generics.ListAPIView):
    serializer_class = PromptTemplateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PromptTemplate.objects.filter(is_public=True)
