# bloomboard/forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = BBProfile
        fields = ['firstName', 'lastName', 'city', 'yearsExperience', 'image_url']
        labels = {
            'firstName': 'Your First Name:',
            'lastName': 'Your Last Name:',
            'city': 'City:',
            'yearsExperience': 'Years of Experience:',
            'image_url': 'Profile Image URL:'
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = BBProfile
        # Exclude the first name and last name from being updated
        fields = ['city', 'yearsExperience', 'image_url']
        labels = {
            'city': 'City:',
            'yearsExperience': 'Years of Experience:',
            'image_url': 'Profile Image URL:'
        }

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['content']
        labels = {
            'content': 'Your Post:'
        }


