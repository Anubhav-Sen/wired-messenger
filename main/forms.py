from django import forms
from django.forms import ModelForm

class LoginForm(forms.Form):

    """
    This class defines all of the fields of the login form.
    """
    
    email = forms.CharField(label='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
