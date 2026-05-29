from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


def settings_view(request):
    return render(request, "pages/settings.html")
