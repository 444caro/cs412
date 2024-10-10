# mini_fb/views.py`
# define the views for the mini_fb app`
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *

# Create your views here.

# class based view 
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile #the model to display
    template_name = 'mini_fb/show_all_profiles.html' #the template to use
    context_object_name = 'profiles' #model describes one profile, so we use the plural form for the context variable 
    
class ShowProfilePageView(DetailView):
    """The view to show a profile page for a single user."""
    model = Profile  # The model to display
    template_name = 'mini_fb/show_profile.html'  # The template to use
    context_object_name = 'profile'  # The context variable name to access the profile in the template
    
