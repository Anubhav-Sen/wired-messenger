from django.db import models
from django.conf import settings
from wiredAPI.models.contact_model import Contact

class Message(models.Model):
    """
    This class models the message.
    It specifies the fields required for a message.
    It defines methods for the message object.
    """
    MESSAGE_CHOICES = (("TEXT", "Text"),("IMAGE", "Image"),("VIDEO", "Video"))

    message_id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    reciver = models.ForeignKey(Contact, on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=5, choices=MESSAGE_CHOICES, default='TEXT')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return f'sent-by: {self.sender}, to: {self.reciver}, msg-type: {self.msg_type}'