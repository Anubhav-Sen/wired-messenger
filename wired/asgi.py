"""
ASGI config for wired project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import path
from channels.auth import AuthMiddlewareStack
import main.routing 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wired.settings')

django_asgi_app = get_asgi_application()

protocols = {
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(URLRouter(main.routing.websocket_urlpatterns))
}

application = ProtocolTypeRouter(protocols)