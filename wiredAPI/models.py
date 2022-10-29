from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

def user_profile_directory_path(instance, filename):

    """
    This function creates a path for a user specific profile 
    directory which stores files related to the users profile.
    """

    return f'user_{instance.user_id}/profile/{filename}'

class UserManager(BaseUserManager):

    """
    This class defines methods required to manage custom "User" model.
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
        This method creates a new user with administrative privilages and adds them to the database.
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

class User(AbstractBaseUser):

    """
    This class models the custom django user, specifies the fields required for login, 
    and defines methods for the user object.
    """

    user_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_name = models.CharField(max_length=50, unique=True)
    email_address = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    bio = models.CharField(max_length=500, null=True, blank=True)
    display_pic = models.ImageField(upload_to=user_profile_directory_path, null=True, blank=True, default='')
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
        This method checks if a user has a certain permission.
        """

        return self.is_admin

    def has_module_perms(self, app_label):

        """
        This method checks if a user has permission to access models in a given app.
        """

        return True

