import json
from unittest import mock
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.authtoken.models import Token

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
        self.user = get_user_model().objects.create_user(first_name = 'test', last_name = 'test', user_name = 'test', email_address = 'test@test.com', password = 'password')
        self.token = Token.objects.create(user=self.user)

    def test_authenticate_user_view_POST(self):
        """
        This function tests the post method of the authenticate user view.
        It asserts if the authenticate user view returns ok when valid credentials are submitted.
        It asserts if the authenticate user view returns bad request when invalid credentials are submitted.
        It asserts if the authenticate user view returns bad request when incorrect credentials are submitted.
        It asserts if the authenticate user view returns a dictionary that contains the expected key value pairs when credentials are valid.
        It asserts if the authenticate user view returns a dictionary that contains the key "errors" when credentials are invalid.
        It asserts if the authenticate user view returns a dictionary that contains the key "errors" when credentials are incorrect.
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

        expected_response_dict = {
            'token-key':self.token.key, 
            'user_id': self.user.user_id, 
            'email_address':self.user.email_address,
            }

        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)
        incorrect_data_response = self.client.post(self.url, data=incorrect_request_dict)

        self.assertEquals(valid_data_response.status_code, 200)
        self.assertEquals(invalid_data_response.status_code, 400)
        self.assertEquals(incorrect_data_response.status_code, 400)

        self.assertDictEqual(valid_data_response.data, expected_response_dict)
        self.assertIn('errors', str(invalid_data_response.data.keys()))
        self.assertIn('errors', str(incorrect_data_response.data.keys()))

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

    def test_create_user_view_POST(self):
        """
        This function tests the post method of the create users view.
        It asserts if the create user view returns created when valid information is submitted.
        """
        valid_request_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test',
            'email_address': 'test@test.com',
            'password': 'password'
        }

        invalid_request_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test',
            'email_address': 'not an email',
            'password': 'password' 
        }

        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)

        self.assertEquals(valid_data_response.status_code, 201)
        self.assertEquals(invalid_data_response.status_code, 400)