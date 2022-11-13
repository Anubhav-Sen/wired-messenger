from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth import get_user_model
from wiredAPI.storage import OverwriteStorage

def user_profile_directory_path(instance, filename):

    """
    This function creates a path for a user specific profile 
    directory which stores files related to the users profile.
    """
    ext = filename.split('.')[-1]
    filename = f'display_pic_user_{instance.user_id}.{ext}'
    return f'user_{instance.user_id}/profile/{filename}'

class UserQuerySet(models.query.QuerySet):
    """
    This class defines custom methods for the user model query sets.
    """
    def update_user(self, **kwargs):
        """
        This method updates a given user.
        If an user id is passed to it, it dosent do attribute assignment.
        If an email address is passed to it, it normalizes the email.
        If a password is passed to it, it hashes the password.
        """
        user = self.first()
        
        for key, value in kwargs.items():
            
            if key == 'user_id':
                pass

            elif key == 'email_address':
                user.email_address = UserManager.normalize_email(value)

            elif key == 'password':
                user.set_password(value)

            else:
                setattr(user, key, value)

        user.save()
    
        return user
    
    def delete_user(self):
        """
        This method deletes a given user.
        """      
        user = self.first()
        user.delete()

class UserManager(BaseUserManager):
    """
    This class defines methods required to manage custom "User" model.
    It normalizes the email passed to it.
    It hashes the password passed to it.
    """
    def create_user(self, email_address, user_name, first_name, last_name, password):
        """
        This method creates a new user and adds them to the database.
        """
        if not email_address:
            raise ValueError('Email address is required to create user.')
        
        if not user_name:
            raise ValueError('Username is required to create user.')
        
        if not first_name:
            raise ValueError('First name is required to create user.')

        if not last_name:
            raise ValueError('Last name is required to create user.')

        if not password:
            raise ValueError('password is required to create user.')

        user = self.model(
            email_address = self.normalize_email(email_address),
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email_address, user_name, first_name, last_name, password):
        """
        This method creates a new user with and adds them to the database.
        It sets the attibutes of new user to make them a super user with administrative privilages.
        """  
        user = self.create_user(
            email_address = self.normalize_email(email_address),
            user_name = user_name,
            first_name = first_name,
            last_name = last_name,
            password=password
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True

        user.save(using=self._db)

        return user

    def get_queryset(self):
        """
        This method returns the custom query set of the user model.
        """
        return UserQuerySet(self.model, using=self._db)
        
class User(AbstractBaseUser):
    """
    This class models the custom django user.
    It specifies the fields required for user.
    It defines methods for the user object.
    """
    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email_address = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    bio = models.CharField(max_length=500, null=True, blank=True)
    display_pic = models.ImageField(upload_to=user_profile_directory_path, storage=OverwriteStorage(), null=True, blank=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email_address'
    REQUIRED_FIELDS = ['user_name', 'first_name', 'last_name', 'password'] 

    objects = UserManager()

    def __str__(self):
        return self.email_address

    def has_perm(self, perm, obj=None): 
        """
        This method checks if a user has admin permissions.
        """
        return self.is_admin

    def has_module_perms(self, app_label):
        """
        This method checks if a user has permission to access models in a given app.
        It returns true for all since this model should have access to all models.
        """
        return True    