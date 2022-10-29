from django.shortcuts import render
from . forms import LoginForm, SignUpForm

def index(request):

    """
    This function defines the main view of the application.
    """
    context = {}
    return render(request, "index.html", context)

def login_view(request):

    """
    This function defines the login view of the application.
    """
    
    login_form = LoginForm()

    context = {'login_form': login_form}
    
    return render(request, "login.html", context)

def register_view(request):

    """
    This function defines the register view of the application.
    """
    signup_form = SignUpForm()

    context = {'signup_form': signup_form}

    return render(request, "signup.html", context)