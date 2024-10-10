from django import forms
from .models import Profile

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
