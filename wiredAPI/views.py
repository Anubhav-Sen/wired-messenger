from django.contrib.auth import get_user_model, authenticate
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from .models import *

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

    authentication_serializer = AuthenticationSerializer(data=request.data)
    
    if authentication_serializer.is_valid():

        user = authenticate(email_address = email_address, password = password)
        
        if user is not None:
            
            token, created = Token.objects.get_or_create(user=user)

            user_serializer = UserSerializer(user)
            
            return Response({'user_data': user_serializer.data,'token_key': token.key}, status=status.HTTP_200_OK)

        else:
            return Response({'errors': {'credentials':('Incorrect email or password.', 'invalid')}}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({'errors':authentication_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def users(request):
    """
    This function defines the POST request to the "users" endpoint. 
    It uses its request data to create a new object, adds it to the database, and returns the object as a responce.
    In case there is an error adding an user to the database the endpoint returns a JSON dictionary of errors as a responce.
    """
    first_name = request.data.get('first_name')
    last_name = request.data.get('last_name')
    user_name = request.data.get('user_name')
    email_address = request.data.get('email_address')
    password = request.data.get('password')
    
    user_serializer = UserSerializer(data=request.data)

    if user_serializer.is_valid():
        
        user = get_user_model().objects.create_user(
            first_name = first_name, 
            last_name = last_name, 
            user_name = user_name, 
            email_address = email_address, 
            password = password
            )
            
        token = Token.objects.create(user=user) 

        user_serializer = UserSerializer(user)

        return Response({'user_data': user_serializer.data,'token_key': token.key}, status=status.HTTP_201_CREATED)

    else:
        return Response({'errors' : user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)          

@api_view(['GET', 'PATCH'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user(request, user_id):
    """
    This function defines the GET request to "user/<int:user_id>" endpoint. 
    It serves an user object in JSON for a given user_id provided to it.
    If the user dosen't exist the endpoint returns a JSON dictionary of erros.
    This function also defines the PATCH request to "users/<int:user_id>" endpoint.
    It uses its request data to update and existing user and returns the updated user object as a responce.
    In case there is an error while updating an user the endpoint returns a JSON dictionary of errors as a responce.
    """
    if request.method == 'GET':

        user = get_user_model().objects.filter(user_id = user_id).first()

        user_serializer = UserSerializer(user)

        if user:
            return Response({'user_data': user_serializer.data}, status=status.HTTP_200_OK)

        else:
            return Response({'errors': {'Resource': ('This user does not exist.', 'dose not exist')}}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PATCH':

        current_user = request.user

        user = get_user_model().objects.filter(user_id = user_id).first()

        if not user:

            return Response({'errors': {'Resource': ('This user does not exist.', 'dose not exist')}}, status=status.HTTP_404_NOT_FOUND)

        if current_user.user_id == user_id:

            update_user_serializer = UpdateUserSerializer(data=request.data)

            if update_user_serializer.is_valid():
                
                update_dict = update_user_serializer.validated_data

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

                user_serializer = UserSerializer(user)

                return Response({'user_data': user_serializer.data,'token_key': token.key}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': update_user_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'errors': {'Authorization': ("You are not authorized to change this object.",'unauthorized')}}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET','POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chats(request):
    """
    This function defines GET requests to the "chats" endpoint.
    It uses the requests user to filter chats and sends back all of the users chats in JSON.
    If the user has no chats the endpoint returns a JSON dictionary of errors.
    This also function defines POST requests to the "chats" endpoint.
    It uses its request data to create a new chat and returns the created chat object as a responce.
    In case there is an error while creating a chat the endpoint returns a JSON dictionary of errors as a responce.
    """
    if request.method == 'GET':

        chats = Chat.objects.filter(participants__model_user = request.user).all()

        chat_serializer = ChatSerializer(chats, many=True)

        if chats:
            return Response({'user_chats': chat_serializer.data}, status=status.HTTP_200_OK)
    
        else:
            return Response({'errors': {'Resource':('This user has no chats.', 'does not exist')}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':

        display_name = request.data.get('display_name')
        email_address = request.data.get('email_address')

        create_chat_serializer = CreateChatSerializer(data=request.data)
        
        if create_chat_serializer.is_valid():

            user = get_user_model().objects.get(email_address = email_address)
        
            if email_address != request.user.email_address:

                existing_chat = Chat.objects.filter(participants__model_user = user).filter(participants__model_user = request.user).first()

                if existing_chat:
                    
                    return Response({'errors': {'Model': ('This chat aldready exists.','already exists')}}, status=status.HTTP_400_BAD_REQUEST)

                if not display_name:

                    display_name = user.user_name

                chat = Chat.objects.create(display_name = display_name)

                Participant.objects.create(model_user = request.user, chat = chat)
                Participant.objects.create(model_user = user, chat = chat)

                chat_serializer = ChatSerializer(chat)
                
                return Response({'chat_data': chat_serializer.data}, status = status.HTTP_201_CREATED)

            else:
                return Response({'errors': {'Field': ("You can't be in a chat with yourself.",'field conflict')}}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            return Response({'errors': create_chat_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','PATCH','DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def chat(request, chat_id):
    """
    This function defined GET requests to the "chats/<int:chat_id>".
    It returns serves a chat object in JSON for a given chat_id. 
    It filters the chat using both the request user and the chat_id as not to allow unauthorized users to access a chat.
    If the chat does not exist or the user is unauthorized the endpoint returns a json dictionary of errors.
    """
    if request.method == 'GET':
        
        chat = Chat.objects.filter(chat_id = chat_id).first()
        user_chat = Chat.objects.filter(participants__model_user = request.user).filter(chat_id = chat_id).first()

        chat_serializer = ChatSerializer(user_chat)

        if chat and user_chat:
            return Response({'chat_data':chat_serializer.data}, status=status.HTTP_200_OK)
        
        elif chat and not user_chat:
            return Response({'errors':{'Authorization':('You are not authorized to view this object.', 'unauthorized')}}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'errors':{'Resource':('This chat does not exist.', 'does not exist')}}, status=status.HTTP_401_UNAUTHORIZED)

    if request.method == 'PATCH':

        display_name = request.data.get('display_name')

        chat = Chat.objects.filter(chat_id = chat_id).first()
        user_chat = Chat.objects.filter(participants__model_user = request.user).filter(chat_id = chat_id).first()
    
        if chat and user_chat:
            
            update_chat_serializer = UpdateChatSerializer(data=request.data)
        
            if update_chat_serializer.is_valid():

                user_chat.display_name = display_name
                user_chat.save()
   
                chat_serializer = ChatSerializer(user_chat)

                return Response({'chat_data': chat_serializer.data}, status=status.HTTP_200_OK)

            else:
                return Response({'errors': update_chat_serializer.errors}, status=status.HTTP_404_NOT_FOUND)

        elif chat and not user_chat:
            
            return Response({'errors':{'Authorization':('You are not authorized to update this object.', 'unauthorized')}}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'errors': {'Resource': ('This chat does not exist.', 'dose not exist')}}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':

        chat = Chat.objects.filter(chat_id = chat_id).first()
        user_chat = Chat.objects.filter(participants__model_user = request.user).filter(chat_id = chat_id).first()

        chat_display_name = user_chat.display_name

        if chat and user_chat:

            user_chat.delete()

            return Response({'message': f'The chat object {chat_display_name} has been deleted.'}, status=status.HTTP_200_OK)
        
        elif chat and not user_chat:
            return Response({'errors':{'Authorization':('You are not authorized to delete this object.', 'unauthorized')}}, status=status.HTTP_404_NOT_FOUND)

        else:
            return Response({'errors':{'Resource':('This chat does not exist.', 'does not exist')}}, status=status.HTTP_401_UNAUTHORIZED)
