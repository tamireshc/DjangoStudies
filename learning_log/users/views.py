from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.


def logout_view(request):
    """Logout do usuário"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))
