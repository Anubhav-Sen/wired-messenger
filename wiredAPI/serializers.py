from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """
    This class serializes the selected fields of the user model into a python dictionary.
    It also validates fields passed to it.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'user_id',
            'first_name',
            'last_name', 
            'user_name', 
            'email_address',
            'password',
            'bio',
            'display_pic',
        ]
        extra_kwargs = {'password': {'write_only': True}}

class AuthenticationSerializer(serializers.Serializer):
    """
    This class serializes authentication fields into a python dictionary.
    It also validates fields passed to it.
    """
    email_address = serializers.EmailField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

class UpdateUserSerializer(serializers.ModelSerializer):
    """
    This class serializes update fields into a python dictionary.
    It also validates fields passed to it.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name',
            'user_name', 
            'password',
            'bio',
            'display_pic',
            ]
        extra_kwargs = {  
            'first_name': {'required': False, 'allow_null': True},
            'last_name': {'required': False, 'allow_null': True},
            'user_name': {'required': False, 'allow_null': True},
            'password': {'required': False, 'allow_null': True},
            'bio': {'required': False, 'allow_null': True},
            'display_pic': {'required': False, 'allow_null': True}
        }

class EmailSerializer(serializers.Serializer):
    """
    This class serializes an email field into a python dictionary.
    It also validates fields passed to it.
    """
    email_address = serializers.EmailField(max_length=255, write_only=True, required=True)

class ChatSerializer(serializers.ModelSerializer):
    """
    This class serializes chat fields into a python dictionary.
    It also validates fields passed to it.
    """
    pass
