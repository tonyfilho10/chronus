import json
import re
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Prompt


def _md_to_html(md: str) -> str:
    html = md
    html = re.sub(r"&", "&amp;", html)
    html = re.sub(r"<(?!/?(?:h[1-3]|li|ul|ol|pre|code|p|strong|hr|br))", "&lt;", html)
    html = re.sub(r"```[\w]*\n?([\s\S]*?)```", r"<pre><code>\1</code></pre>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    html = re.sub(r"^={4,}.*$", "<hr>", html, flags=re.MULTILINE)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"^\s*[-•]\s+(.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = html.replace("\n\n", "</p><p>")
    return f"<p>{html}</p>"


@login_required
def generate_view(request):
    template_id = request.GET.get("template")
    prefill = ""
    if template_id:
        from apps.templates_library.models import PromptTemplate
        try:
            tpl = PromptTemplate.objects.get(pk=template_id)
            prefill = tpl.description
        except PromptTemplate.DoesNotExist:
            pass
    return render(request, "pages/generate.html", {"prefill": prefill})


@login_required
def prompt_list_view(request):
    qs = Prompt.objects.filter(
        user=request.user,
        status__in=[Prompt.Status.SAVED, Prompt.Status.ARCHIVED],
        deleted_at__isnull=True,
    )
    q = request.GET.get("q", "").strip()
    if q:
        qs = qs.filter(Q(title__icontains=q) | Q(idea_input__icontains=q))
    stack = request.GET.get("stack", "")
    if stack:
        qs = qs.filter(stack_target=stack)

    paginator = Paginator(qs, 12)
    page = paginator.get_page(request.GET.get("page"))
    available_stacks = (
        Prompt.objects.filter(user=request.user)
        .values_list("stack_target", flat=True)
        .distinct()
    )
    return render(request, "pages/prompts_list.html", {
        "prompts": page,
        "available_stacks": available_stacks,
    })


@login_required
def prompt_detail_view(request, pk):
    prompt = get_object_or_404(Prompt, pk=pk, deleted_at__isnull=True)
    if not prompt.is_public and prompt.user != request.user:
        return redirect("/prompts/")
    rendered = _md_to_html(prompt.generated_content) if prompt.generated_content else ""
    return render(request, "pages/prompt_detail.html", {
        "prompt": prompt,
        "rendered_content": rendered,
        "raw_content": json.dumps(prompt.generated_content),
    })
