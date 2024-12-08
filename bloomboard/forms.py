# bloomboard/forms.py
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

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

class BaseFlowerUsageFormSet(BaseInlineFormSet):
    def clean(self):
        """Override the default clean method to ignore blank rows."""
        super().clean()
        for form in self.forms:
            if not self.can_delete or not form.cleaned_data.get('DELETE', False):
                # Check if the form is completely empty; if so, skip validation
                if not form.cleaned_data.get('flower') and not form.cleaned_data.get('quantity'):
                    continue
                # Validate partially filled rows
                if form.cleaned_data.get('flower') and not form.cleaned_data.get('quantity'):
                    form.add_error('quantity', 'This field is required if a flower is selected.')
                if not form.cleaned_data.get('flower') and form.cleaned_data.get('quantity'):
                    form.add_error('flower', 'This field is required if a quantity is provided.')
                    
                    
# Inline formset for FlowerUsage
FlowerUsageFormSet = inlineformset_factory(
    Arrangement,  # Parent model
    FlowerUsage,  # Related model
    fields=['flower', 'quantity'],  # Fields to include
    extra=5,  # Number of empty forms to display
    can_delete=True,  # Allow users to remove flowers from the arrangement
    formset=BaseFlowerUsageFormSet
)


class UpdateArrangementForm(forms.ModelForm):
    class Meta:
        model = Arrangement
        fields = ['occassion', 'type', 'image', 'vase']
        labels = {
            'occassion': 'Occasion:',
            'type': 'Arrangement Type:',
            'image': 'Image URL:',
            'vase': 'Vase (Optional):',
        }    

