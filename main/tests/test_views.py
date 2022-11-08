from unittest import mock
from django.test import TestCase, Client
from django.urls import reverse
from main.mocks.mocked_api import mocked_requests_post_login_view, mocked_requests_post_register_view

class TestLoginViewWhileLoggedOut(TestCase):
    """
    This class tests the login view when user is logged out.
    """
    def setUp(self):
        """
        This function defines the set up required to test the login view.
        """
        self.client = Client()
        self.url = reverse('login')

    def test_login_view_GET(self):
        """
        This function tests the get method of the login view.
        It asserts if the connection to the login view is successful.
        It asserts if the login view uses the "login.html" template. 
        """
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    @mock.patch('main.views.requests.post', side_effect=mocked_requests_post_login_view)
    def test_login_view_POST(self, mocked_post):
        """
        This function tests the post method of the login view.
        It asserts if the login view redirects to index when correct login credentials are submitted.
        It asserts if the login view remains as is when the incorrect login credentials are submitted.
        """
        incorrect_request_dict = {
            'email_address':'test@test.com', 
            'password':'incorrect'
            }

        correct_request_dict = {
            'email_address':'test@test.com', 
            'password':'test'
            }

        incorrect_credential_response = self.client.post(self.url, data=incorrect_request_dict)
        correct_credential_response = self.client.post(self.url, data=correct_request_dict)
        
        self.assertEqual(incorrect_credential_response.status_code, 200)
        self.assertRedirects(correct_credential_response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestLoginViewWhileLoggedIn(TestCase):
    """
    This class tests the login view while user is logged in.
    """
    def setUp(self):
        """
        This function defines the set up required to test the login view.
        """
        self.client = Client()
        self.url = reverse('login')
        self.session = self.client.session
        self.session['token-key'] = 'test-token'

        self.session['user-data'] = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'password': 'hashed-password',
            'bio': 'this is a bio',
            'display_pic': None
        }

        self.session.save()
        
    def test_login_view_GET(self):
        """
        This function tests the get method of the login view.
        It asserts if the login view redirects to index when it is accessed as the user is already logged in.
        """        
        response = self.client.get(self.url)

        self.assertRedirects(response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestRegisterView(TestCase):
    """
    This class tests the register view.
    """
    def setUp(self):
        """
        This function defines the set up required to test the register view.
        """
        self.client = Client()
        self.url = reverse('sign-up')

    def test_register_view_GET(self):
        """
        This function tests the get method of the register view.
        It asserts if the connection to the register view is successful.
        It asserts if the register view uses the "signup.html" template. 
        """
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
    
    @mock.patch('main.views.requests.post', side_effect=mocked_requests_post_register_view)
    def test_register_view_POST(self, mockec_post):
        """
        This function tests the post method of the register view.
        It asserts if the register view redirects to login when valid information is submitted.
        It asserts if the register view remains as is when the invalid information is submitted.
        """   
        invalid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'unique-user', 
            'email_address':'unique-email@test.com', 
            'password':'test', 
            'confirm_password':'test'
            }

        valid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com', 
            'password':'test', 
            'confirm_password':'test'
            }

        expected_responce_dict = {
            'user-data':{
                'first_name':'test', 
                'last_name':'test', 
                'user_name':'test', 
                'email_address':'test@test.com',
                'bio': 'this is a bio',
                'display_pic': None
                },
            'token-key': 'test-token'
            }

        invalid_data_response = self.client.post(self.url, data=invalid_request_dict)
        valid_data_response = self.client.post(self.url, data=valid_request_dict)
        
        self.assertEquals(invalid_data_response.status_code, 200)
        self.assertRedirects(valid_data_response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestLogoutView(TestCase):
    """
    This class tests the logout view while user is logged in.
    """
    def setUp(self):
        """
        This function defines the set up required to test the logout view.
        """
        self.client = Client()
        self.url = reverse('logout')
        self.session = self.client.session
        self.session['token-key'] = 'test-token'

        self.session['user-data'] = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'bio': 'this is a bio',
            'display_pic': None
        }

        self.session.save()
        
    def test_login_view_GET(self):
        """
        This function tests the get method of the logout view.
        It asserts if the logout view redirects to login when it is accessed.
        """        
        response = self.client.get(self.url)

        self.assertRedirects(response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestIndexViewWhileLoggedOut(TestCase):
    """
    This class tests the index view while the user is logged out.
    """
    def setUp(self):
        """
        This function defines the set up required to test the index view.
        """
        self.client = Client()
        self.url = reverse('index')

    def test_index_view_GET(self):
        """
        This function tests the get method of the index view.
        It asserts if the index view redirects to the login view when accessed.
        """
        response = self.client.get(self.url)

        self.assertRedirects(response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)


class TestIndexViewWhileLoggedIn(TestCase):
    """
    This class tests the index view while the user is logged in.
    """
    def setUp(self):
        """
        This function defines the set up required to test the index view.
        """
        self.client = Client()
        self.url = reverse('index')
        self.session = self.client.session
        self.session['token-key'] = 'test-token'

        self.session['user-data'] = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'password': 'hashed-password',
            'bio': 'this is a bio',
            'display_pic': None
        }

        self.session.save()

    def test_index_view_GET(self):
        """
        This function tests the get method of the index view.
        It asserts if the connection to the index view is successful.
        It asserts if the connection to the index view is successful when the partial template header profile side area is in the request.
        It asserts if the connection to the index view is successful when the partial template header chat list side area is in the request.
        It asserts if the index view uses the "index.html" template. 
        It asserts if the index view uses the "index.html" template when the profile side area is in the request header values.
        It asserts if the index view uses the "index.html" template when the chat list side area is in the request header values.
        """
        
        response = self.client.get(self.url)
        partial_template_profile_response = self.client.get(self.url, **{'HTTP_Partial-Template':'profile-side-area'})
        partial_template_chat_list_response = self.client.get(self.url, **{'HTTP_Partial-Template':'chat-list-side-area'})
        
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(partial_template_profile_response, 'profile.html')
        self.assertTemplateUsed(partial_template_chat_list_response, 'chat-list.html')