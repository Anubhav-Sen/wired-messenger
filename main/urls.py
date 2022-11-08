from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login', views.login_view, name='login'),
    path('sign-up', views.register_view, name='sign-up'),
    path('logout', views.logout_view, name='logout'),
]