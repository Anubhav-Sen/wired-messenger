from django.test import TestCase
from wiredAPI.serializers import UserSerializer, AuthenticationSerializer
from datetime import datetime, timedelta

class TestSerializers(TestCase):
    """
    This class tests serializers.
    """
    def test_authentication_serializer(self):
        """
        This function tests the authentication serializer.
        Is asserts true if the data passed to it is valid.  
        It aseerts false if the data passed to it is invalid.
        """

        valid_data_dict = {
            'email_address': 'test@test.com',
            'password': 'password'
        }

        invalid_data_dict = {
            'email_address': 'not an email',
            'password': 'password'
        }

        serializer_valid_data = AuthenticationSerializer(data=valid_data_dict)
        serializer_invalid_data = AuthenticationSerializer(data=invalid_data_dict)

        self.assertTrue(serializer_valid_data.is_valid())  
        self.assertFalse(serializer_invalid_data.is_valid())  

    def test_user_serializer(self):
        """
        This function tests the user serialzier.
        Is asserts true if the data passed to it is valid.    
        It asserts false if the data passed to it is invalid.
        """
        
        valid_data_dict = {
            'first_name':'test',
            'last_name':'test',
            'user_name':'test',
            'email_address': 'test@test.com',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
            'date_created': datetime(2022, 11, 5),
            'date_modified': datetime(2022, 11, 5),
        }

        invalid_data_dict = {
            'first_name':'test',
            'last_name':'test',
            'user_name': None,
            'email_address': 'not and email',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
            'date_created': 'not a date',
            'date_modified': 'not a date',
        }

        serializer_valid_data = UserSerializer(data=valid_data_dict)
        serializer_invalid_data = UserSerializer(data=invalid_data_dict)

        self.assertTrue(serializer_valid_data.is_valid())  
        self.assertFalse(serializer_invalid_data.is_valid())  