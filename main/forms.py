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
    This class defines all of the fields of the sign-up form.
    """
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Last Name'}))
    user_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    email_address = forms.EmailField(label='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email Address'}))
    password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))
    confirm_password = forms.CharField(label='', max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password'}))

class EditProfileForm(forms.Form):
    """
    This class defines all of the fields of the edit profile form.
    """
    display_pic = forms.ImageField(label='', required=False, widget=forms.FileInput(attrs={'id':'display-pic-input', 'hidden':'true', 'accept':'image/*'}))  
    first_name = forms.CharField(label='', required=False, max_length=50, widget=forms.TextInput(attrs={'id':'first-name-input', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='', required=False, max_length=50, widget=forms.TextInput(attrs={'id':'last-name-input', 'placeholder': 'Last Name'}))
    user_name = forms.CharField(label='', required=False, max_length=50, widget=forms.TextInput(attrs={'id':'user-name-input','placeholder': 'Username'}))
    bio = forms.CharField(label='', required=False, max_length = 500, widget=forms.Textarea(attrs={'id':'bio-input', 'placeholder': 'Bio'}))

class ChangePasswordForm(forms.Form):
    """
    This class defines all of the fields of the change password form.
    """
    new_password = forms.CharField(label='', required=False, max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'New password', 'readonly':'true'}))
    confirm_password = forms.CharField(label='', required=False, max_length=255, widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'readonly':'true'})) 

class CreateChatForm(forms.Form):
    """
    This class defines all of the fields of the create chat form.
    """
    display_name = forms.CharField(label='Chat display name', label_suffix='', required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Display name'}))
    email_address = forms.EmailField(label='Chat email address', label_suffix='', max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Email address'})) 

class EditChatForm(forms.Form):
    """
    This class defines all of the fields of the edit chat form.
    """
    display_name = forms.CharField(label='Chat display name', label_suffix='', required=False, max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Display name'}))
    
class MessageForm(forms.Form):
    """
    This class defines all of the fields of the message form.
    """
    message_text = forms.CharField(label='', required=False, widget=forms.Textarea(attrs={'placeholder': 'Text message', 'id':'message_text_input', 'rows': 1, 'cols': None}))

