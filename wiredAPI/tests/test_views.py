from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from wiredAPI.serializers import *
from wiredAPI.models import *

class TestAunthenticateUserView(TestCase):
    """
    This class tests the authenticate user view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the authenticate user view.
        """
        self.client = APIClient()
        self.url = reverse('authenticate-user')
        self.user = get_user_model().objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
            )
        self.token = Token.objects.create(user=self.user) 
        self.user_serializer = UserSerializer(self.user)
        self.maxDiff = None

    def test_authenticate_user_view_POST(self):
        """
        This function tests the post method of the authenticate user view.
        It asserts if the authenticate user view returns ok when valid credentials are submitted.
        It asserts if the authenticate user view returns bad request when invalid credentials are submitted.
        It asserts if the authenticate user view returns bad request when incorrect credentials are submitted.
        It asserts if the authenticate user view returns a dictionary that contains the expected key value pairs when credentials are valid.
        It asserts if the authenticate user view returns a dictionary that contains the expected key value pairs when credentials are invalid.
        It asserts if the authenticate user view returns a dictionary that contains the expected key value pairs when credentials are incorrect.
        """
        valid_request_dict = {
            'email_address':'test@test.com',
            'password':'password'
        }

        invalid_request_dict = {
            'email_address':'not an email',
            'password':'password'
        }

        incorrect_request_dict = {
            'email_address':'test@test.com',
            'password':'not the password'
        }

        invalid_request_serializer = AuthenticationSerializer(data = invalid_request_dict)
        invalid_request_serializer.is_valid()
        
        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)
        incorrect_data_response = self.client.post(self.url, data=incorrect_request_dict)

        valid_expected_response_dict = {
            'user_data': self.user_serializer.data,
            'token_key': self.token.key, 
        }

        invalid_expected_response_dict = {
            'errors':invalid_request_serializer.errors, 
            }

        incorrect_expected_response_dict = {
            'errors': {
                'credentials':('Incorrect email or password.', 'invalid'),
                }
            }

        self.assertEquals(valid_data_response.status_code, 200)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertEquals(incorrect_data_response.status_code, 400)

        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)       
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  
        self.assertDictEqual(incorrect_data_response.data, incorrect_expected_response_dict)

class TestUsersView(TestCase):
    """
    This class tests the users view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the users view.
        """
        self.client = APIClient()
        self.url = reverse('users')
        self.maxDiff = None

    def test_users_view_POST(self):
        """
        This function tests the post method of the users view.
        It asserts if the users view returns created when valid information is submitted.
        It asserts if the users view returns bad request when in valid information is submitted.
        It asserts if the users view returns a dictionary that contains the expected key value pairs the information provided is valid.
        It asserts if the users view returns a dictionary that contains the expected key value pairs the information provided is invalid.
        """
        valid_request_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test',
            'email_address': 'test@test.com',
            'password': 'password'
        }

        invalid_request_dict = {
            'first_name': 'test2',
            'last_name': 'test2',
            'user_name': 'test2',
            'email_address': 'not an email',
            'password': 'password' 
        }

        invalid_request_serializer = UserSerializer(data = invalid_request_dict)
        invalid_request_serializer.is_valid()

        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)

        user = get_user_model().objects.get(email_address = 'test@test.com')
        token = Token.objects.get(user = user)

        valid_expected_response_user = UserSerializer(user)

        valid_expected_response_dict = {
            'user_data': valid_expected_response_user.data,
            'token_key':  token.key, 
        }

        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors, 
            }

        self.assertEquals(valid_data_response.status_code, 201)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)    
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  

class TestUserView(TestCase):
    """
    This class tests the user view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the user view.
        """
        self.client = APIClient()
        self.existing_user = get_user_model().objects.create_user(
            first_name = 'extest', 
            last_name = 'extest', 
            user_name = 'extest', 
            email_address = 'extest@test.com', 
            password = 'expassword'
            )
        self.user = get_user_model().objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
            )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('user', kwargs={'user_id': self.user.user_id})
        self.maxDiff = None

    def test_user_view_PATCH(self):
        """
        This function tests the patch method of the user view.  
        It asserts if the user view returns ok when valid information is submitted.
        It asserts if the user view returns bad request when invalid information is submitted.
        It asserts if the user view returns unauthorized when the user_id of another user is passed as an argument.
        It asserts if the user view returns a dictionary that contains the expected key value pairs the information provided is valid.
        It asserts if the user view returns a dictionary that contains the expected key value pairs the information provided is invalid.
        It asserts if the user view returns a dictionary that contains the expected key value pairs the when the user_id of another is passed as an argument.
        """
        valid_request_dict = {
            'first_name': 'updated-fn',
            'last_name': 'updated-ln',
            'user_name': 'updated-un',
            'bio': 'updated-bio',
            'password': 'updated-pw'
        }

        invalid_request_dict = {   
            'first_name': 'updated-fn',
            'last_name': 'updated-ln',
            'user_name': 'extest',
            'bio': 'updated-bio',
            'password': 'updated-pw'
        }

        valid_request_serializer = UpdateUserSerializer(data = valid_request_dict)
        valid_request_serializer.is_valid()

        invalid_request_serializer = UpdateUserSerializer(data = invalid_request_dict)
        invalid_request_serializer.is_valid()

        unauthorized_user_response = self.client.patch(reverse('user', kwargs={'user_id': self.existing_user.user_id}), **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        valid_data_response = self.client.patch(self.url, data=valid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        invalid_data_response = self.client.patch(self.url, data=invalid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
              
        user = get_user_model().objects.get(user_id = self.user.user_id)

        user_serializer = UserSerializer(user)

        valid_expected_response_dict = {
            'user_data': user_serializer.data,
            'token_key':  self.token.key, 
        }

        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors, 
            }

        unauthorized_user_expected_responce_dict = {
            'errors': {'Authorization': ("You are not authorized to change this object.",'unauthorized')}
        }

        self.assertEquals(valid_data_response.status_code, 200)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertEquals(unauthorized_user_response.status_code, 401)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)    
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  
        self.assertDictEqual(unauthorized_user_response.data, unauthorized_user_expected_responce_dict)           

class TestChats(TestCase):
    """
    This class tests the chats view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the chats view.
        """
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
            )
        self.user2 = get_user_model().objects.create_user(
            first_name = 'test2', 
            last_name = 'test2', 
            user_name = 'test2', 
            email_address = 'test2@test.com', 
            password = 'password2'
            )
        self.user3 = get_user_model().objects.create_user(
            first_name = 'test3', 
            last_name = 'test3', 
            user_name = 'test3', 
            email_address = 'test3@test.com', 
            password = 'password3'
            )
        self.token = Token.objects.create(user=self.user1)
        self.url = reverse('chats')
        self.maxDiff = None

    def test_chats_view_GET(self):
        """
        This function tests the get method of the chats view.
        It asserts if the chats view returns ok when the user_id of another user is passed as an argument.
        It asserts if the update user view returns a dictionary that contains the expected key value pairs the information provided is valid.
        """

        chat1 = Chat.objects.create()
        Participant.objects.create(chat = chat1, model_user = self.user1)
        Participant.objects.create(chat = chat1, model_user = self.user2)
  
        chat2 = Chat.objects.create()
        Participant.objects.create(chat = chat2, model_user = self.user1)
        Participant.objects.create(chat = chat2, model_user = self.user3)
                
        response = self.client.get(self.url, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})

        chats = Chat.objects.filter(participants__model_user = self.user1).all()

        chats_serializer = ChatSerializer(chats, many = True)

        expected_response_dict = {
            'user_chats': chats_serializer.data
        }

        self.assertEqual(response.status_code, 200)
        self.assertDictEqual(response.data, expected_response_dict)

    def test_chats_view_POST(self):
        """
        This function tests the get method of the chats view.
        It asserts if the chats view returns ok when valid information is submitted.
        It asserts if the chats view returns bad request when invalid information is submitted.
        It asserts if the chats view returns bad request when a existing user email is is submitted.
        It asserts if the chats view returns bad request when the email of thee user that is making the request is submitted.
        It asserts if the chats view returns a dictionary that contains the expected key value pairs the information provided is valid.
        It asserts if the chats view returns a dictionary that contains the expected key value pairs the information provided is invalid.
        It asserts if the chats view returns a dictionary that contains the expected key value pairs the information provided belongs to an existing user.  
        It asserts if the chats view returns a dictionary that contains the expected key value pairs the information provided belongs to the user making the request.
        """
        
        existing_chat = Chat.objects.create()
        Participant.objects.create(chat = existing_chat, model_user = self.user1)
        Participant.objects.create(chat = existing_chat, model_user = self.user3)

        valid_request_dict = {
            'display_name': 'test-name',
            'email_address': 'test2@test.com'
        }

        invalid_request_dict = {
            'display_name': 'test-name',
            'email_address': 'not an email'
        }

        existing_user_request_dict = {
            'display_name': 'test-name',
            'email_address': 'test3@test.com'
        }

        same_user_request_dict = {
            'display_name': 'test-name',
            'email_address': 'test@test.com'
        }

        valid_data_response = self.client.post(self.url, data=valid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})   
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        exisiting_user_data_response = self.client.post(self.url, data=existing_user_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        same_user_data_response = self.client.post(self.url, data=same_user_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
 
        invalid_request_serializer = CreateChatSerializer(data=invalid_request_dict)
        invalid_request_serializer.is_valid()
 
        chat = Chat.objects.get(participants__model_user = self.user2)

        chat_serializer = ChatSerializer(chat)

        valid_expected_response_dict = {
            'chat_data': chat_serializer.data
        }
        
        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors
        }

        existing_user_expected_response_dict = {
            'errors': {'Model': ('This chat aldready exists.','already exists')}
        }

        same_user_expected_response_dict = {
            'errors':{'Field': ("You can't be in a chat with yourself.",'field conflict')}
        }

        self.assertEqual(valid_data_response.status_code, 201)
        self.assertEqual(invalid_data_response.status_code, 400)
        self.assertEqual(exisiting_user_data_response.status_code, 400)
        self.assertEqual(same_user_data_response.status_code, 400)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)
        self.assertDictEqual(exisiting_user_data_response.data, existing_user_expected_response_dict)
        self.assertDictEqual(same_user_data_response.data, same_user_expected_response_dict)  