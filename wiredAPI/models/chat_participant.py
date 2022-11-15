from django.db import models
from django.conf import settings
from wiredAPI.models import Chat

class Participant(models.Model):
    """
    This class models the participant.
    It specifies the fields required for a participant.
    It defines methods for the participant.
    """
    participant_id = models.BigAutoField(primary_key=True)
    model_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE, related_name='participants')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['chat', 'model_user'], name='unique_chat_and_participant_combination')
        ]

    def __str__(self):
        """
        This method defines the string to be returned for the model object.
        """
        return f'Paticipant: {self.model_user}, Chat: {self.chat}'