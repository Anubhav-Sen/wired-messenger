from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import get_user_model
from wiredAPI.views import *

class TestUris(TestCase):
    """
    This class tests if API views are bound to uris correctly.
    """
    def setUp(self):
        """
        This fuction defines the set up for testing the API uris.
        """
        self.user = get_user_model().objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test',
            email_address = 'test@test.com', 
            password = 'test-password'
        )

    def test_authenticate_user_uri(self):
        
        url = reverse('authenticate-user')

        self.assertEquals(resolve(url).func, authenticate_user)

    def test_users_uri(self):

        url = reverse('users')

        self.assertEquals(resolve(url).func, users)
    
    def test_user_uri(self):
        
        url = reverse('user', kwargs={'user_id': 1})

        self.assertEquals(resolve(url).func, user)

    def test_chats_uri(self):

        url = reverse('chats')

        self.assertEquals(resolve(url).func, chats)