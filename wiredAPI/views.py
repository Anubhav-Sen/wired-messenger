from django.shortcuts import render
from django.http import HttpResponse

def users(request):
    """
    This is the users endpoint, it serves up all of the user objects in JSON.
    """
    return HttpResponse("user data")