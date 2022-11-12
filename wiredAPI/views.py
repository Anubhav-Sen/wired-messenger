from django.contrib.auth import get_user_model, authenticate
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, AuthenticationSerializer, UpdateUserSerializer
from .models import User

@api_view(['POST'])
def authenticate_user(request):
    """
    This function defines the "authenticate-user" endpoint.
    It authenticates a user using provided user credentials.
    If the user is authenticated it returns a JSON responce containing a authorization token, the user's id, and email address.
    If there is an issue authenticating the user it returns a JSON dictionary of errors as a responce.
    """
    email_address = request.data.get('email_address')
    password = request.data.get('password')

    serializer = AuthenticationSerializer(data=request.data)
    
    if serializer.is_valid():

        user = authenticate(email_address = email_address, password = password)
        
        if user is not None:
            
            token, created = Token.objects.get_or_create(user=user)

            display_pic_url = None

            if user.display_pic:
                display_pic_url = user.display_pic.url

            user_data_dict = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_name': user.user_name,
                'email_address': user.email_address,
                'bio': user.bio or None,
                'display_pic': display_pic_url,
            }

            return Response({'user-data': user_data_dict,'token-key': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'errors': {'credentials':('Incorrect email or password', 'invalid')}}, status=status.HTTP_400_BAD_REQUEST)

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
    This function defines the "users/create" endpoint. 
    It uses its request data to create a new object, adds it to the database, and returns the object as a responce.
    In case there is an error adding an user to the database the endpoint returns a JSON dictionary of errors as a responce.
    """
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    user_name = request.data.get('user_name')
    email_address = request.data.get('email_address')
    password = request.data.get('password')
    
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        
        user = get_user_model().objects.create_user(
            first_name = first_name, 
            last_name = last_name, 
            user_name = user_name, 
            email_address = email_address, 
            password = password
            )
            
        token = Token.objects.create(user=user) 

        display_pic_url = None
        
        if user.display_pic: 
            display_pic_url = user.display_pic.url

        user_data_dict = {
                'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'user_name': user.user_name,
                'email_address': user.email_address,
                'bio': user.bio or None,
                'display_pic': display_pic_url
            }

        return Response({'user-data': user_data_dict,'token-key': token.key}, status=status.HTTP_201_CREATED)

    else:
        return Response({'errors' : serializer.errors}, status=status.HTTP_400_BAD_REQUEST)          


@api_view(['PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_user(request, user_id):
    """
    This function defines the "users/<int:user_id/update>" endpoint.
    It uses its request data to updated and existing user and returns the updated user object as a responce.
    In case there is an error while updating an user the endpoint returns a JSON dictionary of errors as a responce.
    """
    current_user = request.user
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    user_name = request.data.get('user_name')
    bio = request.data.get('bio')  
    display_pic = request.FILES.get('display_pic')
    password = request.data.get('password') or None

    if current_user.user_id == user_id:

        serializer = UpdateUserSerializer(data=request.data)

        if serializer.is_valid():

            update_dict = {
                'first_name': first_name,
                'last_name': last_name,
                'user_name': user_name,
                'bio': bio,
                'password': password,
                'display_pic': display_pic
            }

            null_values = []

            for key, value in update_dict.items():

                if value == None and key != 'bio':
                    null_values.append(key)

                if value == None and key == 'bio':
                    value = ''

            for value in null_values:
                update_dict.pop(value)

            user = get_user_model().objects.filter(user_id = user_id).update_user(**update_dict)

            token = Token.objects.get(user=user) 

            display_pic_url = None

            if user.display_pic: 
                display_pic_url = user.display_pic.url

            user_data_dict = {
                    'user_id': user.user_id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'user_name': user.user_name,
                    'email_address': user.email_address,
                    'bio': user.bio or None,
                    'display_pic': display_pic_url
                }

            return Response({'user-data': user_data_dict,'token-key': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    else:
        return Response({'errors': {'Authorization': ("You are not authorized to change this object.",'unauthorized')}}, status=status.HTTP_401_UNAUTHORIZED)