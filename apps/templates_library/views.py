from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.templates_library.models import PromptTemplate


@login_required
def templates_view(request):
    cat = request.GET.get('cat', '')
    qs = PromptTemplate.objects.filter(is_public=True)
    if cat:
        qs = qs.filter(category=cat)
    categories = PromptTemplate.Category.choices
    return render(request, 'pages/templates_library.html', {
        'templates': qs,
        'categories': categories,
    })
