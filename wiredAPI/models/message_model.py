from django.db import models
from django.conf import settings
from wiredAPI.models.chat_model import Chat

class Message(models.Model):
    """
    This class models the message.
    It specifies the fields required for a message.
    It defines methods for the message object.
    """
    MESSAGE_CHOICES = (("TEXT", "Text"),("IMAGE", "Image"),("VIDEO", "Video"))

    message_id = models.BigAutoField(primary_key=True)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='receiver')
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    msg_type = models.CharField(max_length=5, choices=MESSAGE_CHOICES, default='TEXT')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return f'Sent-by: {self.sender}, To: {self.reciver}, Msg-type: {self.msg_type}, In: {self.chat}'