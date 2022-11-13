from django.db import models
from wiredAPI.models.message_model import Message

class Chat(models.Model):
    """
    This class models the chat.
    It specifies the fields required for a chat.
    It defines methods for the chat object.
    """
    chat_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)