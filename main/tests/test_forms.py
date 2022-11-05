from django.test import SimpleTestCase
from main.forms import LoginForm, SignUpForm

class TestForms(SimpleTestCase):
    """
    This class tests forms.
    """

    def test_login_form(self):
        """
        This function tests the login form.
        Is asserts true if the data passed to it is valid.
        It asserts false if the data passed to it is invalid.
        """

        valid_data_dict = {
            'email_address': 'test@test.com',
            'password': 'password'
        }

        invalid_data_dict = {
            'email_address': 'not an email',
            'password': 'password'
        }

        login_form_valid_data = LoginForm(data=valid_data_dict)
        login_form_invalid_data = LoginForm(data=invalid_data_dict)

        self.assertTrue(login_form_valid_data.is_valid())  
        self.assertFalse(login_form_invalid_data.is_valid())  

    def test_sign_up_form(self):
        """
        This function tests the sign up form.
        It asserts true if the data passed to it is valid.
        It asserts false if the data passed to it is invalid.
        """
        
        valid_data_dict = {
            'first_name':'test',
            'last_name':'test',
            'user_name':'test',
            'email_address': 'test@test.com',
            'password': 'password',
            'confirm_password': 'password'
        }

        invalid_data_dict = {
            'first_name':'test',
            'last_name':'test',
            'user_name':'test',
            'email_address': 'not an email',
            'password': 'password',
            'confirm_password': 'password'
        }

        signup_form_valid_data = SignUpForm(data=valid_data_dict)
        signup_form_invalid_data = SignUpForm(data=invalid_data_dict)

        self.assertTrue(signup_form_valid_data.is_valid())  
        self.assertFalse(signup_form_invalid_data.is_valid())  