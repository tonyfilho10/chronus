from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from apps.prompts.models import Prompt
from apps.community.models import Upvote


@login_required
def community_view(request):
    # CSHUB: todos os prompts salvos da equipe são visíveis internamente (sem necessidade de is_public)
    qs = Prompt.objects.filter(
        status="saved",
        deleted_at__isnull=True,
    ).order_by("-created_at")

    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(idea_input__icontains=q))

    stack = request.GET.get("stack", "")
    if stack:
        qs = qs.filter(stack_target=stack)

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    available_stacks = (
        Prompt.objects.filter(status="saved", deleted_at__isnull=True)
        .values_list("stack_target", flat=True)
        .distinct()
    )
    user_upvotes = set(
        Upvote.objects.filter(user=request.user).values_list("prompt_id", flat=True)
    )

    return render(request, "pages/community.html", {
        "prompts": page,
        "available_stacks": available_stacks,
        "user_upvotes": user_upvotes,
    })
