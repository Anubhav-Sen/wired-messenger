import os
from django.core.files.storage import FileSystemStorage
from django.conf import settings

class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=None):
        """
        This function returns a filename thats avaiable in the media root directory for a new file to be written to.
        If a name is not available it deletes the file with that name and returns the name to facilitiate overwritting.
        """
        self.delete(name)
        return name