from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, AuthenticateUserSerializer
from .models import User

@api_view(['GET', 'POST'])
def users(request):
    """
    This function defines the "users" endpoint. 
    Tt serves all of the user objects in JSON.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)  

@api_view(['GET'])
def user(request, user_id):
    """
    This function defines the "user/<int:user_id>" endpoint. 
    It serves an user object in JSON for a given user_id provided to it .
    """
    user = User.objects.get(user_id = user_id)
    serializer = UserSerializer(user)

    return Response(serializer.data)

@api_view(['POST'])
def authenticate_user(request):
    """
    This function defines the "user/authenticate" endpoint. 
    It authenticates an user and returns the authenticated user object as a responce.
    In case a user cannot be authenticated it returns status code 400 to indicate a bad request.
    """

    email_address = request.data['email_address']
    password = request.data['password']

    serializer = AuthenticateUserSerializer(data=request.data)

    if serializer.is_valid():

        user = authenticate(request, email_address = email_address, password = password)
        
        if user is not None:
            
            return Response({'user':user}, status=status.HTTP_200_OK)
    
    else:

        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def create_user(request):
    """
    This function defines the "user/create" endpoint. 
    It posts a JSON user object and adds it to the database and returns the object as a responce.
    In case there is an error adding a user to the database the endpoint returns a dictionary of errors as a responce.
    """
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    user_name = request.data['user_name']
    email_address = request.data['email_address']
    password = request.data['password']
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        
        get_user_model().objects.create_user(first_name = first_name, last_name = last_name, user_name = user_name, email_address = email_address, password = password)

        serializer.validated_data['password'] = make_password(password)

        return Response({'user': serializer.validated_data}, status=status.HTTP_201_CREATED)

    else:
        return Response({'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)          