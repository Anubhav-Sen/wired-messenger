import requests
import json
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from . forms import *
from . custom_decorators import login_required

@login_required(login_url='login')
@require_http_methods(['GET', 'POST', 'DELETE'])
def index_view(request):
    """
    This function defines the main view of the application.
    It renders the "index.html" template.
    It also returns rendered partial templates with their respective forms.
    """
    user_data = request.session['user_data']
    token_key = request.session['token_key']
    
    headers = {'Authorization': f'token {token_key}'}
    chats_uri = f'{request.scheme}://{request.get_host()}/api/chats'
    
    chats_get_responce = requests.get(chats_uri, headers=headers)
    chats_get_dict = json.loads(chats_get_responce.content)

    create_chat_form = CreateChatForm()
    edit_chat_form = EditChatForm()
    message_form = MessageForm()

    context = {
        'user_data': user_data,
        'chats': chats_get_dict,
        'create_chat_form': create_chat_form,
        'message_form': message_form,
        'edit_chat_form': edit_chat_form, 
    }

    if request.method == 'DELETE':

        chat_id = request.headers.get('Chat-Id')
        print(chat_id)

        chat_uri = f'{request.scheme}://{request.get_host()}/api/chats/{chat_id}' 

        chat_post_responce = requests.delete(chat_uri, headers=headers)

        if chat_post_responce.status_code == 200:

            return HttpResponse(status=200)
        
    if request.method == 'POST' and request.headers.get('Index-Page-Form') == 'create-chat-form':
        
        display_name = request.POST.get('display_name')
        email_address = request.POST.get('email_address')

        request_dict = {
            'display_name': display_name,
            'email_address': email_address
        }
        
        chats_post_responce = requests.post(chats_uri, json=request_dict, headers=headers)
        chats_post_dict = json.loads(chats_post_responce.content)
   
        if chats_post_responce.status_code == 201:

            return HttpResponse(status=200)

        elif chats_post_responce.status_code == 400:
            
            for value in chats_post_dict['errors'].values():
                
                return JsonResponse({'error': '*' + str(value[0])}, status=400)
    
    elif request.method == 'POST' and request.headers.get('Index-Page-Form') == 'edit-chat-form':
  
        chat_id = request.headers.get('Chat-Id')
        chat_uri = f'{request.scheme}://{request.get_host()}/api/chats/{chat_id}'

        display_name = request.POST.get('display_name')

        request_dict = {
            'display_name': display_name,
        }
        
        chat_post_responce = requests.patch(chat_uri, json=request_dict, headers=headers)
        chat_post_dict = json.loads(chat_post_responce.content)
   
        if chat_post_responce.status_code == 200:

            display_name = chat_post_dict['chat_data']['display_name']
            
            return JsonResponse({'display_name': display_name}, status=200)

        elif chat_post_responce.status_code == 400:
            
            for value in chat_post_dict['errors'].values():
                
                return JsonResponse({'error': '*' + str(value[0])}, status=400)

    if request.method == 'GET' and request.headers.get('Partial-Template') == 'profile-side-area':

        return render(request, "profile.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'chat-list-side-area':
             
        return render(request, "chat-list.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'create-chat-side-area':
        
        return render(request, "create-chat.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'chat-window':
        
        chat_id = request.headers.get('Chat-Id')
        chat_uri = f'{request.scheme}://{request.get_host()}/api/chats/{chat_id}'
        
        chat_get_responce = requests.get(chat_uri, headers=headers)
        chat_get_dict = json.loads(chat_get_responce.content)

        context['chat'] = chat_get_dict['chat_data']
        
        return render(request, "chat-window.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'chat-window-closed':
        
        return render(request, "chat-window-closed.html", context)

    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'chat-participant-profile-side-area':

        chat_id = request.headers.get('Chat-Id')
        chat_uri = f'{request.scheme}://{request.get_host()}/api/chats/{chat_id}'
        
        chat_get_responce = requests.get(chat_uri, headers=headers)
        chat_get_dict = json.loads(chat_get_responce.content)

        context['chat'] = chat_get_dict['chat_data']
    
        return render(request, "chat-participant-profile.html", context)
    
    elif request.method == 'GET' and request.headers.get('Partial-Template') == 'edit-chat-side-area':

        chat_id = request.headers.get('Chat-Id')

        context['chat_id'] = chat_id
    
        return render(request, "edit-chat.html", context)
        
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
    
    if request.session.get('token_key'):

       return redirect('index')

    if request.method == 'POST':
        
        email_address = request.POST.get('email_address')
        password = request.POST.get('password')

        request_dict = {
            'email_address': email_address,
            'password' : password
        }

        request_uri = f'{request.scheme}://{request.get_host()}/api/authenticate-user'

        api_responce = requests.post(request_uri, json=request_dict)
        response_dict = json.loads(api_responce.content)

        if api_responce.status_code == 200:

            request.session['token_key'] = response_dict['token_key']
            request.session['user_data'] = response_dict['user_data']

            return redirect('index')

        elif api_responce.status_code == 400:

            for value in response_dict['errors'].values():

                messages.error(request, '*' + str(value[0]))
                break

    login_form = LoginForm()

    context = {'login_form': login_form}
    
    return render(request, "login.html", context)


@login_required(login_url='login')
@require_http_methods(['GET'])
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
    If there is an issue creating a user it adds a error message to the django "messages" dictionary.
    """
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

            request_uri = f'{request.scheme}://{request.get_host()}/api/users'

            api_responce = requests.post(request_uri, json=request_dict)

            if api_responce.status_code == 201:
            
                return redirect('login')
        
            elif api_responce.status_code == 400:

                errors = json.loads(api_responce.content) 

                for value in errors['errors'].values():

                    messages.error(request, '*' + str(value[0]))
                    break
                
        else:  
            messages.error(request, "*The passwords entered don't match.")
    
    signup_form = SignUpForm()

    context = {'signup_form': signup_form}

    return render(request, 'signup.html', context)

@login_required(login_url='login')
@require_http_methods(['GET', 'POST'])
def edit_profile_view(request):
    """
    This function defines the edit profile view of the application.
    It renders the edit profile form.
    It makes an api request to update an existing user.
    It redirects to the main view of the application if the user is successfully updated and no password change occurs.
    In case of a password change it redirects to the logout view of the application.
    If there is an issue updating a user it adds a error message to the django "messages" dictionary.
    """
    user_data = request.session['user_data']
    token_key = request.session['token_key']

    if request.method == 'POST':
 
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_name = request.POST.get('user_name')
        bio = request.POST.get('bio')
        files = request.FILES
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
       
        user_id = user_data['user_id']
        headers = {'Authorization': f'token {token_key}'}
        request_uri = f'{request.scheme}://{request.get_host()}/api/users/{user_id}'

        api_responce = None
        
        request_dict = {  
                'first_name': first_name or None,
                'last_name': last_name or None,
                'user_name': user_name or None,
                'bio': bio,
                'password': new_password or None,
        }

        if user_name == None or user_name == user_data['user_name']:

            request_dict.pop('user_name')

        if not new_password:
        
            api_responce = requests.patch(request_uri, data=request_dict, files = files, headers=headers)
            response_dict = json.loads(api_responce.content)

            if api_responce.status_code == 200:

                request.session['token_key'] = response_dict['token_key']
                request.session['user_data'] = response_dict['user_data']
      
                return redirect('index')

            elif api_responce.status_code == 400 or api_responce.status_code == 401:

                errors = json.loads(api_responce.content) 

                for value in errors['errors'].values():
    
                    messages.error(request, '*' + str(value[0]))
                    break

        elif new_password and new_password == confirm_password:

            api_responce = requests.patch(request_uri, data=request_dict, files = files, headers=headers)
       
            if api_responce.status_code == 200:
                    
                return redirect('logout')   

            elif api_responce.status_code == 400 or api_responce.status_code == 401:

                errors = json.loads(api_responce.content) 

                for value in errors['errors'].values():
                    
                    messages.error(request, '*' + str(value[0]))
                    break
        else: 
            messages.error(request, "*The passwords entered don't match.")

    edit_profile_form_data = {
        'first_name':user_data['first_name'],
        'last_name':user_data['last_name'],
        'user_name':user_data['user_name'],
        'bio':user_data['bio'],
    }

    edit_profile_form = EditProfileForm(data=edit_profile_form_data)
    change_password_form = ChangePasswordForm()

    context = {
        'user_data':user_data,
        'edit_profile_form': edit_profile_form,
        'change_password_form': change_password_form,
    }

    return render(request, 'edit-profile.html', context)