# mini_fb/forms.py
from django import forms
from .models import Profile
from .models import StatusMessage
from django.contrib.auth.forms import UserCreationForm

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['firstName', 'lastName', 'city', 'email', 'image_url']
        labels = {
            'firstName': 'Your First Name:',
            'lastName': 'Your Last Name:',
            'city': 'City:',
            'email': 'Email Address:',
            'image_url': 'Profile Image URL:'
        }

        
class CreateStatusMessageForm(forms.ModelForm):
    class Meta:
        model = StatusMessage
        fields = ['message']
        labels = {
            'message': 'Status Message:'
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        # Exclude the first name and last name from being updated
        fields = ['city', 'email', 'image_url']
        labels = {
            'city': 'City:',
            'email': 'Email Address:',
            'image_url': 'Profile Image URL:'
        }
