import json
from unittest import mock
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token
from wiredAPI.serializers import AuthenticationSerializer, UserSerializer

class TestAunthenticateUserView(TestCase):
    """
    This class tests the authenticate user view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the authenticate user view.
        """
        self.client = Client()
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
            'token-key':self.token.key, 
            'user_id': self.user.user_id, 
            'email_address':self.user.email_address,
            }

        invalid_expected_response_dict = {
            'errors':invalid_request_serializer.errors, 
            }

        incorrect_expected_response_dict = {
            'errors': {
                'credentials':('Incorrect email or password', 'InvalidCredentials'),
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
        self.client = Client()
        self.url = reverse('create-user')
        self.maxDiff = None

    def test_create_user_view_POST(self):
        """
        This function tests the post method of the create users view.
        It asserts if the create user view returns created when valid information is submitted.
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

        user = get_user_model().objects.filter(email_address = 'test@test.com').first()
        token = Token.objects.get(user = user)

        valid_request_serializer.validated_data['password'] = user.password

        valid_expected_response_dict = { 
            'user_data': valid_request_serializer.validated_data, 
            'token-key': token.key,
            }

        invalid_expected_response_dict = {
            'errors': invalid_request_serializer.errors, 
            }

        self.assertEquals(valid_data_response.status_code, 201)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertDictEqual(valid_data_response.data, valid_expected_response_dict)       
        self.assertDictEqual(invalid_data_response.data, invalid_expected_response_dict)  