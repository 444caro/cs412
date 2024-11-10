# voter_analytics/forms.py
from django import forms
from .models import Voter

class VoterFilterForm(forms.Form):
    '''Form for filtering voters'''
    # Dropdown for party affiliation, with a blank option for no filter
    PARTY_CHOICES = [
        ('', 'Any'),
        ('D', 'Democratic'),
        ('R', 'Republican'),
        ('CC', 'Constitution Party'),
        ('L', 'Libertarian Party'),
        ('T', 'Tea Party'),
        ('O', 'Other'),
        ('G', 'Green Party'),
        ('J', 'Independent Party'),
        ('Q', 'Reform Party'),
        ('FF', 'Freedom Party'),
    ]
    party_affiliation = forms.ChoiceField(choices=PARTY_CHOICES, required=False, label="Party Affiliation")
    
    # Dropdowns for minimum and maximum birth years
    BIRTH_YEAR_CHOICES = [(str(year), str(year)) for year in range(1920, 2024)]
    min_birth_year = forms.ChoiceField(choices=[('', 'Any')] + BIRTH_YEAR_CHOICES, required=False, label="Born After Year")
    max_birth_year = forms.ChoiceField(choices=[('', 'Any')] + BIRTH_YEAR_CHOICES, required=False, label="Born Before Year")
    
    # Dropdown for voter score
    VOTER_SCORE_CHOICES = [(str(i), str(i)) for i in range(6)]  # 0 to 5 score
    voter_score = forms.ChoiceField(choices=[('', 'Any')] + VOTER_SCORE_CHOICES, required=False, label="Voter Score")
    
    # Checkboxes for voting in specific elections
    voted_20state = forms.BooleanField(required=False, label="Voted in 2020 State Election")
    voted_21town = forms.BooleanField(required=False, label="Voted in 2021 Town Election")
    voted_21primary = forms.BooleanField(required=False, label="Voted in 2021 Primary Election")
    voted_22general = forms.BooleanField(required=False, label="Voted in 2022 General Election")
    voted_23town = forms.BooleanField(required=False, label="Voted in 2023 Town Election")
    
    def filter_queryset(self, queryset):
        # Filter by party affiliation
        if self.cleaned_data['party_affiliation']:
            queryset = queryset.filter(party_affiliation=self.cleaned_data['party_affiliation'])
        
        # Filter by birth year range
        if self.cleaned_data['min_birth_year']:
            queryset = queryset.filter(date_of_birth__year__gte=int(self.cleaned_data['min_birth_year']))
        if self.cleaned_data['max_birth_year']:
            queryset = queryset.filter(date_of_birth__year__lte=int(self.cleaned_data['max_birth_year']))
        
        # Filter by voter score
        if self.cleaned_data['voter_score']:
            queryset = queryset.filter(voter_score=int(self.cleaned_data['voter_score']))
        
        # Filter by election participation
        if self.cleaned_data['voted_20state']:
            queryset = queryset.filter(v20state=True)
        if self.cleaned_data['voted_21town']:
            queryset = queryset.filter(v21town=True)
        if self.cleaned_data['voted_21primary']:
            queryset = queryset.filter(v21primary=True)
        if self.cleaned_data['voted_22general']:
            queryset = queryset.filter(v22general=True)
        if self.cleaned_data['voted_23town']:
            queryset = queryset.filter(v23town=True)
        
        return queryset
    