from django.urls import path

from . import views

urlpatterns = [
    path('users', views.users, name='users'),
    path('users/<int:user_id>', views.user, name='user'),
    path('authenticate-user', views.authenticate_user, name='authenticate-user'),
    path('chats', views.chats, name='chats')
]