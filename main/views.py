from django.shortcuts import render
from . forms import LoginForm

def index(request):

    """
    This function defines the main view of the application.
    """
    context = {}
    return render(request, "index.html", context)

def login_view(request):

    """
    This function defindes the login view of the application.
    """
    
    login_form = LoginForm()

    context = {'login_form': login_form}
    
    return render(request, "login.html", context)