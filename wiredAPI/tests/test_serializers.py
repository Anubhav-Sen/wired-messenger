from django.test import TestCase
from django.contrib.auth import get_user_model
from wiredAPI.serializers import *
from wiredAPI.models import *
from datetime import datetime, timedelta


class TestSerializers(TestCase):
    """
    This class tests serializers.
    """

    def setUp(self):
        """
        This function defines the set up required to test serializers.
        """
        self.user = get_user_model().objects.create_user(
            first_name='test',
            last_name='test',
            user_name='test',
            email_address='test@test.com',
            password='password'
        )
        self.user2 = get_user_model().objects.create_user(
            first_name='test2',
            last_name='test2',
            user_name='test2',
            email_address='test2@test.com',
            password='password2'
        )
        self.user3 = get_user_model().objects.create_user(
            first_name='test3',
            last_name='test3',
            user_name='test3',
            email_address='test3@test.com',
            password='password3'
        )
        self.existing_chat = Chat.objects.create(display_name='test')
        Participant.objects.create(
            chat=self.existing_chat, model_user=self.user)
        Participant.objects.create(
            chat=self.existing_chat, model_user=self.user2)
        self.maxDiff = None

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
        serializer_invalid_data = AuthenticationSerializer(
            data=invalid_data_dict)

        self.assertTrue(serializer_valid_data.is_valid())
        self.assertFalse(serializer_invalid_data.is_valid())

    def test_user_serializer(self):
        """
        This function tests the user serialzier.
        It asserts if the serializer can serialize a model instance. 
        It asserts true if the data passed to it is valid.    
        It asserts false if the data passed to it is invalid.
        """

        valid_data_dict = {
            'user_id': 4,
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test4',
            'email_address': 'test4@test.com',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
        }

        invalid_data_dict = {
            'user_id': 1,
            'first_name': 'test',
            'last_name': 'test',
            'user_name': None,
            'email_address': 'not and email',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
        }

        model_serializer = UserSerializer(self.user)
        serializer_valid_data = UserSerializer(data=valid_data_dict)
        serializer_invalid_data = UserSerializer(data=invalid_data_dict)

        serialized_data_dict = {
            'user_id': self.user.user_id,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'user_name': self.user.user_name,
            'email_address': self.user.email_address,
            'bio': self.user.bio,
            'display_pic': self.user.display_pic or None,
        }

        self.assertDictEqual(model_serializer.data, serialized_data_dict)
        self.assertTrue(serializer_valid_data.is_valid())
        self.assertFalse(serializer_invalid_data.is_valid())

    def test_update_user_serializer(self):
        """
        This function tests the update user serialzier.  
        It asserts if the serializer can serialize a model instance. 
        Is asserts true if the data passed to it is valid.    
        It asserts false if the data passed to it is invalid.
        """

        valid_data_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test4',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
        }

        invalid_data_dict = {
            'first_name': 'test',
            'last_name': 'test',
            'user_name': 'test',
            'password': 'password',
            'bio': 'test is a bio',
            'display_pic': None,
        }

        model_serializer = UpdateUserSerializer(self.user)
        serializer_valid_data = UpdateUserSerializer(data=valid_data_dict)
        serializer_invalid_data = UpdateUserSerializer(data=invalid_data_dict)

        serialized_data_dict = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'user_name': self.user.user_name,
            'password': self.user.password,
            'bio': self.user.bio,
            'display_pic': self.user.display_pic or None,
        }

        self.assertDictEqual(model_serializer.data, serialized_data_dict)
        self.assertTrue(serializer_valid_data.is_valid())
        self.assertFalse(serializer_invalid_data.is_valid())

    def test_create_chat_serializer(self):
        """
        This function tests the create chat serializer.
        Is asserts true if the data passed to it is valid.  
        It aseerts false if the data passed to it is invalid.
        """

        valid_data_dict = {
            'display_name': 'test',
            'email_address': 'test4@test.com'
        }

        invalid_data_dict = {
            'displat_name': 'test',
            'email_address': 'not an email',
        }

        serializer_valid_data = CreateChatSerializer(data=valid_data_dict)
        serializer_invalid_data = CreateChatSerializer(data=invalid_data_dict)

        self.assertTrue(serializer_valid_data.is_valid())
        self.assertFalse(serializer_invalid_data.is_valid())

    def test_chat_serializer(self):
        """
        This function tests the chat user serialzier.  
        It asserts if the serializer can serialize a model instance.
        """

        model_serializer = ChatSerializer(self.existing_chat)

        serialized_data_dict = {
            'chat_id': 1, 
            'display_name': 'test', 
            'participants': [
                {
                    'model_user': {
                        'user_id': self.user.user_id, 
                        'first_name': self.user.first_name, 
                        'last_name': self.user.last_name,
                        'user_name': self.user.user_name, 
                        'email_address': self.user.email_address, 
                        'bio': None, 
                        'display_pic': None
                    }
                },
                {
                    'model_user': {
                        'user_id': self.user2.user_id, 
                        'first_name': self.user2.first_name, 
                        'last_name': self.user2.last_name, 
                        'user_name': self.user2.user_name, 
                        'email_address': self.user2.email_address, 
                        'bio': None, 
                        'display_pic': None
                    }
                }
                ]
            }

        self.assertDictEqual(model_serializer.data, serialized_data_dict)
