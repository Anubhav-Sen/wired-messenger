from webbrowser import get
from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """
    This class serializes the selected fields of the user model into a JSON object.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'first_name',
            'last_name', 
            'user_name', 
            'email_address',
            'password',
            'bio',
            'display_pic',
            'date_created',
            'date_modified',
            ]
        extra_kwargs = {'password': {'write_only': True}}

class AuthenticationSerializer(serializers.Serializer):
    """
    This class serializes authentication fields into a JSON object.
    """
    email_address = serializers.EmailField(max_length=255, write_only=True, required=True)
    password = serializers.CharField(max_length=255, write_only=True, required=True)

class UpdateUserSerializer(serializers.ModelSerializer):
    """
    This class serializes update fields into a JSON object.
    """
    class Meta:
        model = get_user_model()
        fields = [
            'user_name', 
            'password',
            'bio',
            'display_pic',
            ]
        extra_kwargs = {
            'user_name': {'required': False, 'allow_null': True},
            'password': {'required': False, 'allow_null': True},
            'bio': {'required': False, 'allow_null': True},
            'display_pic': {'required': False, 'allow_null': True}
        }