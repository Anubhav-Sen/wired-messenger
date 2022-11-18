
from django.http import HttpResponseRedirect

def login_required(login_url=None):
    """
    This function defines a decorator that checks if a user is logged in. 
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):

            token_key = request.session.get('token_key')  
            user_data = request.session.get('user_data')  

            if (token_key and user_data):

                return function(request, *args, **kwargs)
            
            else:
                return HttpResponseRedirect(login_url)

        return wrapper
    
    return decorator