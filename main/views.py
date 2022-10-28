from django.shortcuts import render
from django.http import HttpResponse

def index(request):

    """
    This is the main view of the application.
    """
    context = {}
    return render(request, "index.html", context)

def login_view(request):

    """
    This is the login view of the application.
    """
    context = {}
    return render(request, "login.html", context)