from django.db import models
from django.conf import settings
from wiredAPI.models.message_model import Message

class TextMessage(models.Model):
    """
    This class models the text message.
    It specifies the fields required for a text message.
    It defines methods for the text message object.
    """
    text_message_id = models.BigAutoField(primary_key=True)
    content = models.TextField()
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    model_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return self.content