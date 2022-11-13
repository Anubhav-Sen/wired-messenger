from django.db import models
from django.conf import settings
from wiredAPI.models.message_model import Message


def image_media_directory_path(instance, filename):
    """
    This function creates a path for a user specific media 
    directory which stores the users media files.
    """
    return f'user_{instance.user_id}/media/{filename}'

class ImageMessage(models.Model):
    """
    This class models the image message.
    It specifies the fields required for a image message.
    It defines methods for the image message object.
    """
    image_message_id = models.BigAutoField(primary_key=True)
    image = models.ImageField(upload_to=image_media_directory_path)
    content = models.TextField(null=True, blank=True)
    message = models.OneToOneField(Message, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)