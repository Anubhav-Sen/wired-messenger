from django.test import TestCase
from django.contrib.auth import get_user_model

class TestUserModel(TestCase):
    """
    This class tests the user model.
    """
    def setUp(self):
        """
        This function defines the set up required to test the user model.
        """
        self.model = get_user_model()

    def test_user_model_create_user(self):
        """
        This function tests the create_user method of the custom user manager.
        It asserts if the new_user object exists.
        """
        new_user = self.model.objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
            )
                
        self.assertEquals(new_user, self.model.objects.get(email_address = 'test@test.com'))

    def test_user_model_update_user(self):
        """
        This function tests the update_user method of the custom user manager.
        It asserts if the initial_user object has changed to reflect the changes made in updated user.
        """
        initial_user = self.model.objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
            )

        updated_user = self.model.objects.filter(email_address = 'test@test.com').update_user(
            first_name = 'updated-fh',
            last_name = 'updated-ln',
            user_name = 'updated-username',
            email_address = 'updated@test.com',
            password = 'updated-password',
            bio = 'This is a bio',
            display_pic = None
            )

        self.assertEquals(initial_user.user_id, updated_user.user_id)
        
    def test_user_model_delete_user(self):
        """
        This function tests the delete_user method of the custom user manager.
        It asserts if the deleted user no longer exists. 
        """
        user = self.model.objects.create_user(
            first_name = 'test', 
            last_name = 'test', 
            user_name = 'test', 
            email_address = 'test@test.com', 
            password = 'password'
        )

        self.model.objects.filter(email_address = 'test@test.com').delete_user()

        self.assertRaises(user.DoesNotExist)