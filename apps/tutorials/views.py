import re
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TutorialCategory, Tutorial


def _md_to_html(md: str) -> str:
    html = md
    html = re.sub(r"&", "&amp;", html)
    html = re.sub(r"```(\w*)\n?([\s\S]*?)```", r"<pre><code class='lang-\1'>\2</code></pre>", html)
    html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
    html = re.sub(r"^### (.+)$", r"<h3>\1</h3>", html, flags=re.MULTILINE)
    html = re.sub(r"^## (.+)$", r"<h2>\1</h2>", html, flags=re.MULTILINE)
    html = re.sub(r"^# (.+)$", r"<h1>\1</h1>", html, flags=re.MULTILINE)
    html = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html)
    html = re.sub(r"\*(.+?)\*", r"<em>\1</em>", html)
    html = re.sub(r"^\s*[-•]\s+(.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"^\d+\.\s+(.+)$", r"<li>\1</li>", html, flags=re.MULTILINE)
    html = re.sub(r"^> (.+)$", r"<blockquote>\1</blockquote>", html, flags=re.MULTILINE)
    html = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2" class="text-[#F97316] hover:underline font-medium" target="_blank">\1</a>', html)
    html = html.replace("\n\n", "</p><p>")
    return f"<p>{html}</p>"


@login_required
def tutorial_list_view(request):
    categories = TutorialCategory.objects.prefetch_related("tutorials").filter(
        tutorials__is_published=True
    ).distinct()
    selected_cat = request.GET.get("cat")
    all_tutorials = Tutorial.objects.filter(is_published=True)
    if selected_cat:
        all_tutorials = all_tutorials.filter(category__slug=selected_cat)

    return render(request, "pages/tutorials.html", {
        "categories": categories,
        "tutorials": all_tutorials,
        "selected_cat": selected_cat,
    })


@login_required
def tutorial_detail_view(request, slug):
    tutorial = get_object_or_404(Tutorial, slug=slug, is_published=True)
    # Next/prev in same category
    siblings = Tutorial.objects.filter(
        category=tutorial.category, is_published=True
    ).order_by("order", "title")
    ids = list(siblings.values_list("id", flat=True))
    idx = ids.index(tutorial.id) if tutorial.id in ids else -1
    prev_tut = siblings.filter(id=ids[idx - 1]).first() if idx > 0 else None
    next_tut = siblings.filter(id=ids[idx + 1]).first() if idx < len(ids) - 1 else None

    return render(request, "pages/tutorial_detail.html", {
        "tutorial": tutorial,
        "rendered_content": _md_to_html(tutorial.content),
        "prev_tutorial": prev_tut,
        "next_tutorial": next_tut,
    })
