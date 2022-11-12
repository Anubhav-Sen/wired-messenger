from unittest import mock
from django.test import TestCase, Client
from django.urls import reverse
from main.mocks.mocked_api import mocked_requests_post_login_view, mocked_requests_post_register_view, mocked_requests_patch_edit_profile_view

class TestLoginView(TestCase):
    """
    This class tests the login view.
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

    def test_login_view_while_logged_in(self):
        """
        This function tests the get method of the login view while user is logged in.
        It asserts if the login view redirects to index when it is accessed as the user is already logged in.
        """
        session = self.client.session
        session['token-key'] = 'test-token'

        session['user-data'] = {
            'user_id': 1,
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'password': 'hashed-password',
            'bio': 'this is a bio',
            'display_pic': None
        }

        session.save()

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
    def test_register_view_POST(self, mocked_post):
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
            'user_id': 1,
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
    
    def test_logout_view_while_logged_out(self):
        """
        This function tests the get method of the logout view while the user is logged out.
        It asserts if the logout view redirects to the login view when accessed.
        """
        self.session.flush()

        response = self.client.get(self.url)

        self.assertRedirects(response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestIndexView(TestCase):
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
            'user_id': 1,
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

    def test_index_view_while_logged_out(self):
        """
        This function tests the get method of the index view while the user is logged out.
        It asserts if the index view redirects to the login view when accessed.
        """
        self.session.flush()

        response = self.client.get(self.url)

        self.assertRedirects(response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)

class TestEditProfileView(TestCase):
    """
    This class tests the edit profile view while the user is logged in.
    """
    def setUp(self):
        """
        This function defines the set up required to test the edit profile view.
        """
        self.client = Client()
        self.url = reverse('edit-profile')
        self.session = self.client.session
        self.session['token-key'] = 'test-token'

        self.session['user-data'] = {
            'user_id': 1,
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'email_address':'test@test.com',
            'password': 'hashed-password',
            'bio': 'this is a bio',
            'display_pic': None
        }

        self.session.save()

    def test_register_view_GET(self):
        """
        This function tests the get method of the edit profile view.
        It asserts if the connection to the edit profile view is successful.
        It asserts if the edit profile view uses the "edit-profile.html" template. 
        """
        response = self.client.get(self.url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit-profile.html')
    
    @mock.patch('main.views.requests.patch', side_effect=mocked_requests_patch_edit_profile_view)
    def test_register_view_POST(self, mocked_post):
        """
        This function tests the post method of the edit profile view.
        It asserts if the edit profile view remains as is when the invalid information is submitted.
        It asserts if the edit profile view redirects to index when valid information is submitted without passwords.
        It asserts if the edit profile view redirects to logout when valid information is submitted and it contains passwords.
        """   
        no_password_invalid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'unique-user',
            }

        password_invalid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'unique-user', 
            'new_password':'test', 
            'confirm_password':'test'
            }

        no_password_valid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test',  
        }

        password_valid_request_dict = {
            'first_name':'test', 
            'last_name':'test', 
            'user_name':'test', 
            'new_password':'test', 
            'confirm_password':'test' 
        }

        no_password_invalid_data_response = self.client.post(self.url, data=no_password_invalid_request_dict)
        password_invalid_data_response = self.client.post(self.url, data=password_invalid_request_dict)
        no_password_valid_data_response = self.client.post(self.url, data=no_password_valid_request_dict)
        password_valid_data_response = self.client.post(self.url, data=password_valid_request_dict)
           
        self.assertEquals(no_password_invalid_data_response.status_code, 200)
        self.assertEquals(password_invalid_data_response.status_code, 200)
        self.assertRedirects(no_password_valid_data_response, '/', status_code=302, target_status_code=200, fetch_redirect_response=True)
        self.assertRedirects(password_valid_data_response, '/logout', status_code=302, target_status_code=302, fetch_redirect_response=True)

    def test_edit_profile_view_while_logged_out(self):
        """
        This function tests the get method of the edit profile view while the user is logged out.
        It asserts if the edit profile view redirects to the login view when accessed.
        """
        self.session.flush()

        response = self.client.get(self.url)

        self.assertRedirects(response, '/login', status_code=302, target_status_code=200, fetch_redirect_response=True)