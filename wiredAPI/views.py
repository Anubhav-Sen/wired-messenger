import email
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from .serializers import UserSerializer, AuthenticationSerializer
from .models import User

@api_view(['POST'])
def authenticate_user(request):
    """
    This function defines the "authenticate-user" endpoint.
    It authenticates a user using provided user credentials.
    If the user is authenticated it returns a JSON responce containing a authorization token, the user's id, and email address.
    If there is an issue authenticating the user it returns a JSON dictionary of errors as a responce.
    """
    email_address = request.data['email_address']
    password = request.data['password']

    serializer = AuthenticationSerializer(data=request.data)
    
    if serializer.is_valid():

        user = authenticate(email_address = email_address, password = password)
        
        if user is not None:
            
            token, created = Token.objects.get_or_create(user=user)

            return Response({'token': token.key, 'user_id':user.user_id,'email_address': user.email_address}, status=status.HTTP_200_OK)

        else:

            return Response({'errors': {'credentials':('Incorrect email or password', 'InvalidCredentials')}}, status=status.HTTP_400_BAD_REQUEST)

    else:

        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def users(request):
    """
    This function defines the "users" endpoint. 
    Tt serves all of the user objects in JSON.
    """
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)

    return Response(serializer.data)  


@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request, user_id):
    """
    This function defines the "user/<int:user_id>" endpoint. 
    It serves an user object in JSON for a given user_id provided to it .
    """
    user = User.objects.get(user_id = user_id)
    serializer = UserSerializer(user)

    return Response(serializer.data)

@api_view(['POST'])
def create_user(request):
    """
    This function defines the "user/create" endpoint. 
    It posts a JSON user object and adds it to the database and returns the object as a responce.
    In case there is an error adding a user to the database the endpoint returns a JSON dictionary of errors as a responce.
    """
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    user_name = request.data['user_name']
    email_address = request.data['email_address']
    password = request.data['password']
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        
        user = get_user_model().objects.create_user(first_name = first_name, last_name = last_name, user_name = user_name, email_address = email_address, password = password)
        token = Token.objects.create(user=user) 

        serializer.validated_data['password'] = make_password(password)

        return Response({'user_data': serializer.validated_data, 'token': token}, status=status.HTTP_201_CREATED)

    else:
        return Response({'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)          