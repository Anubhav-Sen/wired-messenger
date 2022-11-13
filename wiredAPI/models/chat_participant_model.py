from django.db import models
from django.conf import settings
from wiredAPI.models.chat_model import Chat


class ChatParticipant(models.Model):
    """
    This class models the chat participant.
    It specifies the fields required for a chat participant.
    It defines methods for the chat participant object.
    """
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    participant = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)