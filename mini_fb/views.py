# mini_fb/views.py`
# define the views for the mini_fb app`
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from .models import *
from .forms import CreateProfileForm

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
    
class CreateProfileView(CreateView):
    '''The view to create a new profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'

    def get_success_url(self):
        '''Return the URL to display the profile page after creation.'''
        return reverse('show_profile', kwargs={'pk': self.object.pk})

class CreateStatusMessageView(CreateView):
    '''The view to create a new status message.'''
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/create_status_message_form.html'

    def get_success_url(self):
        '''Return the URL to display the profile page after creation.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def form_valid(self, form):
        '''Add the profile to the form data before setting the message profile.'''
        form.instance.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        return super().form_valid(form)