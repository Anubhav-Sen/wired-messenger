from django.db import models
from django.conf import settings

class Chat(models.Model):
    """
    This class models the chat.
    It specifies the fields required for a chat.
    It defines methods for the chat.
    """
    chat_id = models.BigAutoField(primary_key=True)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return self.display_name or f'Chat_{self.chat_id}'