# bloomboard/forms.py

from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.forms.models import BaseInlineFormSet

class CreateProfileForm(forms.ModelForm):
    '''Form for creating a new BBProfile.'''
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
    '''Form for updating an existing BBProfile.'''
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
    """Form for creating a new post."""
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
    '''Form for creating a new Flower.'''
    class Meta:
        model = Flower
        fields = ['name', 'use_type', 'price_per_stem', 'image_url']
        labels = {
            'name': 'Flower Name:',
            'use_type': 'Use Type:',
            'price_per_stem': 'Price per Stem:',
            'image_url': 'Image URL:',
        }
       
class FlowerFilterForm(forms.Form):
    '''Form for filtering flowers by use type.'''
    USE_TYPE_CHOICES = [('filler','Filler'),('focal','Focal'), ('greens','Greens')]
    
    # Use type filter (Dropdown/ChoiceField)
    use_type = forms.ChoiceField(
        choices=[('', 'All')] + USE_TYPE_CHOICES,  # Adding an "All" option for no filtering
        label='Use Type',
        required=False
    )
    
    # Minimum price filter
    min_price = forms.DecimalField(
        label='Minimum Price per Stem',
        required=False,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 1.00'})
    )
    
    # Maximum price filter
    max_price = forms.DecimalField(
        label='Maximum Price per Stem',
        required=False,
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'placeholder': 'e.g., 10.00'})
    )
    
    
    def filter_queryset(self, queryset):
        """Filter the given queryset based on form inputs."""
        # Filter by use type
        use_type = self.cleaned_data.get('use_type')
        if use_type:
            queryset = queryset.filter(use_type=use_type)
        
        # Filter by minimum price
        min_price = self.cleaned_data.get('min_price')
        if min_price is not None:
            queryset = queryset.filter(price_per_stem__gte=min_price)
        
        # Filter by maximum price
        max_price = self.cleaned_data.get('max_price')
        if max_price is not None:
            queryset = queryset.filter(price_per_stem__lte=max_price)
        
        return queryset
    

    

    
    
class CreateVaseForm(forms.ModelForm):
    '''Form for creating a new Vase.'''
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
    '''Form for creating a new Arrangement.'''
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
    """Custom formset to validate partially filled rows."""
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
    '''Form for updating an existing Arrangement.'''
    class Meta:
        model = Arrangement
        fields = ['occassion', 'type', 'image', 'vase']
        labels = {
            'occassion': 'Occasion:',
            'type': 'Arrangement Type:',
            'image': 'Image URL:',
            'vase': 'Vase (Optional):',
        }    

