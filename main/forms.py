from django import forms
from django.forms import ModelForm

class LoginForm(forms.Form):

    """
    This class defines all of the fields of the login form.
    """
    
    email_address = forms.EmailField(label='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))

class SignUpForm(forms.Form):

    """
    This class defines all of the fields of the login form.
    """

    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    user_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email_address = forms.EmailField(label='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))
 