import requests
import json
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import HttpResponseRedirect
from . forms import LoginForm, SignUpForm
from . custom_decorators import login_required

@login_required(login_url='login')
def index(request):

    """
    This function defined the main view of the application.
    """
    context = {'email_address':request.session['email_address']}

    return render(request, "index.html", context)

@require_http_methods(['GET', 'POST'])
def login_view(request):

    """
    This function defines the login view of the application. 
    It renders the login form.
    It makes an api request to authenicate the user.
    It logs in the user by adding the data recieved from the api call to the session dictionary.
    It redirects the user to the main view of the application.
    if there is an issue loging in it adds the error message to the django "messages" dictionary.
    """
    
    login_form = LoginForm()

    if request.method == 'POST':

        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        request_dict = {
            'email_address': email_address,
            'password' : password
        }

        api_request = requests.post(f'{request.scheme}://{request.get_host()}/api/authenticate-user', json=request_dict)
        response_dict = json.loads(api_request.content)

        if api_request.status_code == 200:

            request.session['token'] = response_dict['token']
            request.session['user_id'] = response_dict['user_id']
            request.session['email_address'] = response_dict['email_address']

            return redirect('index')

        elif api_request.status_code == 400:

            for value in response_dict['errors'].values():

                messages.error(request, f'*{value[0]}')
                break

    context = {'login_form': login_form}
    
    return render(request, "login.html", context)

@require_http_methods(['GET'])
@login_required(login_url='login')
def logout_view(request):

    """
    This function defines the logout of view of the applicaion.
    It logs out user by flushing the session data and redirects to the login view.
    """
    request.session.flush()

    return redirect('login')

@require_http_methods(['GET', 'POST'])
def register_view(request):

    """
    This function defines the register view of the application.
    It renders the sign-up form.
    It makes an api request to create a new user.
    It redirects to the login page if a new user is successfully created.
    If there is an issue creating a user it adds the a error message to the django "messages" dictionary.
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