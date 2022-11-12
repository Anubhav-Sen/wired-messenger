import json
from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from wiredAPI.serializers import AuthenticationSerializer, UserSerializer, UpdateUserSerializer

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
            'user-data': {
                'user_id': self.user.user_id,
                'first_name': self.user.first_name, 
                'last_name': self.user.last_name, 
                'user_name':self.user.user_name, 
                'email_address': self.user.email_address,
                'bio': self.user.bio,
                'display_pic': None
            },
            'token-key':self.token.key, 
        }

        invalid_expected_response_dict = {
            'errors':invalid_request_serializer.errors, 
            }

        incorrect_expected_response_dict = {
            'errors': {
                'credentials':('Incorrect email or password', 'invalid'),
                }
            }

        self.assertEquals(valid_data_response.status_code, 200)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertEquals(incorrect_data_response.status_code, 400)

        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)       
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  
        self.assertDictEqual(incorrect_data_response.data, incorrect_expected_response_dict)

class TestCreateUserView(TestCase):
    """
    This class tests the create user view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the create user view.
        """
        self.client = APIClient()
        self.url = reverse('create-user')
        self.maxDiff = None

    def test_create_user_view_POST(self):
        """
        This function tests the post method of the create users view.
        It asserts if the create user view returns created when valid information is submitted.
        It asserts if the create user view returns bad request when in
        valid information is submitted.
        It asserts if the create user view returns a dictionary that contains the expected key value pairs the information provided is valid.
        It asserts if the create user view returns a dictionary that contains the expected key value pairs the information provided is invalid.
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

        valid_request_serializer = UserSerializer(data = valid_request_dict)
        valid_request_serializer.is_valid()

        invalid_request_serializer = UserSerializer(data = invalid_request_dict)
        invalid_request_serializer.is_valid()

        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)

        user = get_user_model().objects.get(email_address = 'test@test.com')
        token = Token.objects.get(user = user)

        valid_expected_response_dict = {
            'user-data': {
                'user_id': user.user_id,
                'first_name': user.first_name, 
                'last_name': user.last_name, 
                'user_name': user.user_name, 
                'email_address': user.email_address,
                'bio': user.bio,
                'display_pic': None,
            },
            'token-key': token.key, 
        }

        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors, 
            }

        self.assertEquals(valid_data_response.status_code, 201)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)    
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  

class TestUpdateUserView(TestCase):
    """
    This class tests the update user view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the update user view.
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
        self.url = reverse('update-user', kwargs={'user_id': self.user.user_id})
        self.maxDiff = None

    def test_update_user_view_PATCH(self):
        """
        This function tests the patch method of the update user view.  
        It asserts if the update user view returns unauthorized when no authorization header is passed.
        It asserts if the update user view returns ok when valid information is submitted.
        It asserts if the update user view returns bad request when invalid information is submitted.
        It asserts if the update user view returns unauthorized when the user_id of another user is passed as an argument.
        It asserts if the update user view returns a dictionary that contains the expected key value pairs the information provided is valid.
        It asserts if the update user view returns a dictionary that contains the expected key value pairs the information provided is invalid.
        It asserts if the update user view returns a dictionary that contains the expected key value pairs the when the user_id of another is passed as an argument.
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

        unauthorized_response = self.client.patch(self.url)
        unauthorized_user_response = self.client.patch(reverse('update-user', kwargs={'user_id': self.existing_user.user_id}), **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        valid_data_response = self.client.patch(self.url, data=valid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
        invalid_data_response = self.client.patch(self.url, data=invalid_request_dict, **{'HTTP_AUTHORIZATION': f'token {self.token.key}'})
       
        valid_expected_response_dict = {
            'user-data': {
                'user_id': self.user.user_id,
                'first_name': 'updated-fn', 
                'last_name': 'updated-ln', 
                'user_name': 'updated-un', 
                'email_address': self.user.email_address,
                'bio': 'updated-bio',
                'display_pic': None,
            },
            'token-key': self.token.key, 
        }

        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors, 
            }

        unauthorized_user_expected_responce_dict = {
            'errors': {'Authorization': ("You are not authorized to change this object.",'unauthorized')}
        }

        self.assertEquals(unauthorized_response.status_code, 401)
        self.assertEquals(valid_data_response.status_code, 200)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertEquals(unauthorized_user_response.status_code, 401)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)    
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  
        self.assertDictEqual(unauthorized_user_response.data, unauthorized_user_expected_responce_dict)           