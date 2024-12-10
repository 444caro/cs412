# bloomboard/forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory

class CreateProfileForm(forms.ModelForm):
    class Meta:
        model = BBProfile
        fields = ['firstName', 'lastName', 'city', 'years_experience', 'image_url']
        labels = {
            'firstName': 'Your First Name:',
            'lastName': 'Your Last Name:',
            'city': 'City:',
            'years_experience': 'Years of Experience:',
            'image_url': 'Profile Image URL:'
        }

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = BBProfile
        # Exclude the first name and last name from being updated
        fields = ['city', 'years_experience', 'image_url']
        labels = {
            'city': 'City:',
            'years_experience': 'Years of Experience:',
            'image_url': 'Profile Image URL:'
        }

class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['caption', 'image', 'arrangement']
        labels = {
            'caption': 'Caption:',
            'image': 'Image URL:',
            'arrangement': 'Arrangement (Optional):',
        }


class UpdatePostForm(forms.ModelForm):
    """Form for updating an existing post."""
    class Meta:
        model = Post
        fields = ['caption', 'image']
        widgets = {
            'caption': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Update your caption here...',
                'rows': 3
            }),
            'image': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Update the image URL here...'
            }),
        }
        
class CreateFlowerForm(forms.ModelForm):
    class Meta:
        model = Flower
        fields = ['name', 'use_type', 'price_per_stem', 'image_url']
        labels = {
            'name': 'Flower Name:',
            'use_type': 'Use Type:',
            'price_per_stem': 'Price per Stem:',
            'image_url': 'Image URL:',
        }
        
class CreateVaseForm(forms.ModelForm):
    class Meta:
        model = Vase
        fields = ['size', 'height', 'color', 'price', 'image_url']
        labels = {
            'size': 'Size:',
            'height': 'Height (inches):',
            'color': 'Color:',
            'price': 'Price:',
            'image_url': 'Image URL:',
        }
        
class CreateArrangementForm(forms.ModelForm):
    class Meta:
        model = Arrangement
        fields = ['profile', 'occassion', 'type', 'image', 'vase']
        labels = {
            'profile': 'Designer Profile:',
            'occassion': 'Occasion:',
            'type': 'Arrangement Type:',
            'image': 'Image URL:',
            'vase': 'Vase (Optional):',
        }
# Inline formset for FlowerUsage
FlowerUsageFormSet = inlineformset_factory(
    Arrangement,  # Parent model
    FlowerUsage,  # Related model
    fields=['flower', 'quantity'],  # Fields to include
    extra=5,  # Number of empty forms to display
    can_delete=True  # Allow users to remove flowers from the arrangement
)
class FlowerUsageForm(forms.ModelForm):
    '''Form for adding a flower usage to an arrangement.'''
    class Meta:
        model = FlowerUsage
        fields = ['flower', 'quantity']
        widgets = {
            'flower': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }
        

