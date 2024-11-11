# /voter_analytics/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm
import plotly.express as px
from plotly.io import to_html

class VoterListView(ListView):
    '''View for displaying a list of voters'''
    model = Voter
    template_name = 'voter_analytics/voter_list.html'
    #context_object_name = 'voters'
    paginate_by = 100
    
    def get_queryset(self):
        '''Filter the queryset based on the form data'''
        queryset = super().get_queryset()
        form = VoterFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter_queryset(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        '''Add the filter form to the context'''
        context = super().get_context_data(**kwargs)
        context['filter_form'] = VoterFilterForm(self.request.GET)
        return context
    
class VoterDetailView(DetailView):
    '''View for displaying a single voter'''
    model = Voter
    template_name = 'voter_analytics/voter_detail.html'
    
    def get_context_data(self, **kwargs):
        '''Add the filter form to the context'''
        context = super().get_context_data(**kwargs)
        voting_history = {
            "2020 State Election": self.object.v20state,
            "2021 Town Election": self.object.v21town,
            "2021 Primary Election": self.object.v21primary,
            "2022 General Election": self.object.v22general,
            "2023 Town Election": self.object.v23town,
        }
        context['voting_history'] = voting_history
        return context


class VoterGraphsView(ListView):
    '''View for displaying graphs of voter data'''
    model = Voter
    template_name = 'voter_analytics/graphs.html'

    def get_context_data(self, **kwargs):
        '''Add the filter form and graphs to the context'''
        context = super().get_context_data(**kwargs)
        form = VoterFilterForm(self.request.GET or None)
        queryset = Voter.objects.all()
        
        # Apply filters if form is valid
        if form.is_valid():
            if form.cleaned_data['party_affiliation']:
                queryset = queryset.filter(party_affiliation=form.cleaned_data['party_affiliation'])
            if form.cleaned_data['min_birth_year']:
                queryset = queryset.filter(date_of_birth__year__gte=form.cleaned_data['min_birth_year'])
            if form.cleaned_data['max_birth_year']:
                queryset = queryset.filter(date_of_birth__year__lte=form.cleaned_data['max_birth_year'])
            if form.cleaned_data['voter_score']:
                queryset = queryset.filter(voter_score=form.cleaned_data['voter_score'])
            for election in ['v20state', 'v21town', 'v21primary', 'v22general', 'v23town']:
                if form.cleaned_data.get(election):
                    queryset = queryset.filter(**{election: True})
        
        # Add filtered queryset and form to context
        context['form'] = form
        context['voters'] = queryset

        # Generate graphs
        context['birth_year_histogram'] = self.create_birth_year_histogram(queryset)
        context['party_affiliation_pie'] = self.create_party_affiliation_pie_chart(queryset)
        context['election_participation_histogram'] = self.create_election_participation_histogram(queryset)

        return context
    
    def create_birth_year_histogram(self, queryset):
        '''Create a histogram of voter birth years'''
        birth_years = [v.date_of_birth.year for v in queryset]
        fig = px.histogram(x=birth_years, title='Distribution of Voters by Birth Year', labels={'x': 'Birth Year', 'y': 'Count'})
        fig.update_layout(bargap=0.2)
        return to_html(fig, full_html=False)

    def create_party_affiliation_pie_chart(self, queryset):
        '''Create a pie chart of voter party affiliations'''
        parties = [v.party_affiliation for v in queryset]
        fig = px.pie(names=parties, title='Distribution of Voters by Party Affiliation')
        return to_html(fig, full_html=False)

    def create_election_participation_histogram(self, queryset):
        '''Create a histogram of voter participation in each election'''
        participation_counts = {
            '2020 State': queryset.filter(v20state=True).count(),
            '2021 Town': queryset.filter(v21town=True).count(),
            '2021 Primary': queryset.filter(v21primary=True).count(),
            '2022 General': queryset.filter(v22general=True).count(),
            '2023 Town': queryset.filter(v23town=True).count()
        }
        fig = px.bar(x=list(participation_counts.keys()), y=list(participation_counts.values()), 
                     title='Voter Participation by Election', labels={'x': 'Election', 'y': 'Count'})
        return to_html(fig, full_html=False)