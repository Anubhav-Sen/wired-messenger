
from django.http import HttpResponseRedirect
from functools import wraps

def login_required(login_url=None):
    """
    This function defines a decorator that checks if a user is logged in. 
    """
    def decorator(function):
        def wrapper(request, *args, **kwargs):

            token = request.session.get('token')  

            if not token:

                return HttpResponseRedirect(login_url)

            else:

                return function(request, *args, **kwargs)

        return wrapper
    
    return decorator