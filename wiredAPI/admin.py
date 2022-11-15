from django.contrib import admin
from . models import *

admin.site.register(User)
admin.site.register(Chat)
admin.site.register(Participant)
admin.site.register(Message)
admin.site.register(TextMessage)
admin.site.register(ImageMessage)
admin.site.register(VideoMessage)
