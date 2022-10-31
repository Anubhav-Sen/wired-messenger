import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse
from . forms import LoginForm, SignUpForm

@login_required(login_url='login')
def index(request):

    """
    This function defined the main view of the application.
    """
    context = {}

    return render(request, "index.html", context)

@require_http_methods(['GET', 'POST'])
def login_view(request):

    """
    This function defines the login view of the application. 
    It renders the login form, authenicates the user, and logs in the user.
    """
    
    login_form = LoginForm()

    if request.method == 'POST':

        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        request_dict = {
            'email_address': email_address,
            'password': password
        }

        api_request = requests.post(f'{request.scheme}://{request.get_host()}/api/user/authenticate', json=request_dict)

        """if user is not None:
            
            login(request, user)

            return redirect('index')

        else:
            messages.error(request, '*Incorrect email or password.')"""

    context = {'login_form': login_form}
    
    return render(request, "login.html", context)

@login_required(login_url='login')
@require_http_methods(['GET'])
def logout_view(request):

    """
    This function defines the logout of view of the applicaion.
    It logs out user and redirects to the login view.
    """
    logout(request)

    return redirect('login')

@require_http_methods(['GET', 'POST'])
def register_view(request):

    """
    This function defines the register view of the application.
    """
    signup_form = SignUpForm()

    if request.method == 'POST':
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
    
        request_dict = {
            'first_name': first_name,
            'last_name': last_name,
            'user_name': user_name,
            'email_address': email_address,
            'password': password
        }
        
        if confirm_password == password:

            api_request = requests.post(f'{request.scheme}://{request.get_host()}/api/user/create', json=request_dict)

            if api_request.status_code == 201:
            
                return redirect('login')
        
            elif api_request.status_code == 400:

                errors = json.loads(api_request.content) 

                for value in errors['errors'].values():

                    messages.error(request, f'*{value[0]}')
                    break
                
        else:
            
            messages.error(request, "*The passwords entered don't match.")
        
    context = {'signup_form': signup_form}

    return render(request, "signup.html", context)