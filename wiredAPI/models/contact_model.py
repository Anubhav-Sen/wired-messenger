from django.db import models
from django.conf import settings

class Contact(models.Model):
    """
    This class models the contact.
    It specifies the fields required for a contact.
    It defines methods for the contact object.
    """
    contact_id = models.BigAutoField(primary_key=True)
    display_name = models.CharField(max_length=255)
    contact_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='contact_user')
    model_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=None, related_name='model_user')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return self.display_name