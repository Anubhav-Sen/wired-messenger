
from django.http import HttpResponseRedirect

def login_required(login_url=None):
    """
    This function defines a decorator that checks if a user is logged in. 
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):

            token_key = request.session.get('token_key')  

            if not token_key:

                return HttpResponseRedirect(login_url)

            else:

                return function(request, *args, **kwargs)

        return wrapper
    
    return decorator