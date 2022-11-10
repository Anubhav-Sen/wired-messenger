from genericpath import exists
import requests
import json
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from . forms import LoginForm, SignUpForm, EditProfileForm
from . custom_decorators import login_required

@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def index_view(request):
    """
    This function defines the main view of the application.
    It renders the "index.html" template.
    It also returns rendered partial templates.
    """

    context = {'user_data':request.session['user-data']}

    if request.method == 'GET' and request.headers.get('Partial-Template') == 'profile-side-area':
        
        return render(request, "profile.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'chat-list-side-area':
        
        return render(request, "chat-list.html", context)

    else:
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
    
    if request.session.get('token-key'):

       return redirect('index')

    if request.method == 'POST':

        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        request_dict = {
            'email_address': email_address,
            'password' : password
        }

        api_responce = requests.post(f'{request.scheme}://{request.get_host()}/api/authenticate-user', json=request_dict)
        response_dict = json.loads(api_responce.content)

        if api_responce.status_code == 200:

            request.session['token-key'] = response_dict['token-key']
            request.session['user-data'] = response_dict['user-data']

            return redirect('index')

        elif api_responce.status_code == 400:

            for value in response_dict['errors'].values():

                messages.error(request, f'*{value[0]}')
                break

    login_form = LoginForm()

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

            api_responce = requests.post(f'{request.scheme}://{request.get_host()}/api/user/create', json=request_dict)

            if api_responce.status_code == 201:
            
                return redirect('login')
        
            elif api_responce.status_code == 400:

                errors = json.loads(api_responce.content) 

                for value in errors['errors'].values():

                    messages.error(request, f'*{value[0]}')
                    break
                
        else:
            
            messages.error(request, "*The passwords entered don't match.")
        
    context = {'signup_form': signup_form}

    return render(request, 'signup.html', context)

@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def edit_profile_view(request):
    """
    This function defines the edit profile view of the application.
    """
    edit_profile_form = EditProfileForm()

    context = {
        'user_data':request.session['user-data'],
        'edit_profile_form': edit_profile_form
        }

    return render(request, 'edit-profile.html', context)