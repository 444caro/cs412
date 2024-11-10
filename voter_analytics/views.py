# /voter_analytics/views.py
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Voter
from .forms import VoterFilterForm

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

