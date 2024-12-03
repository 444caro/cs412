# bloomboard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

# show all flowers
class ShowAllFlowersView(ListView):
    '''the view to show all flowers'''
    model = Flower #the model to display
    template_name = 'bloomboard/show_all_flowers.html' #the template to use
    context_object_name = 'flowers' #model describes one flower, so we use the plural form for the context variable
    #note to self, add feature to see arrangements that use this flower, w the ability to click on the arrangement to see the arrangement post

##        PROFILE VIEWS         ##
# show all profiles
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = BBProfile #the model to display
    template_name = 'bloomboard/show_all_profiles.html' #the template to use
    context_object_name = 'bbprofiles' #model describes one profile, so we use the plural form for the context variable 

# profile detail view 
class ShowProfilePageView(DetailView):
    """The view to show a profile page for a single user."""
    model = BBProfile  # The model to display
    template_name = 'bloomboard/show_profile.html'  # The template to use
    context_object_name = 'bbprofile'  # The context variable name to access the profile in the template
    def get_object(self):
        '''Get the object to display.'''
        return get_object_or_404(BBProfile, user=self.request.user)


# create profile view
class CreateProfileView(CreateView):
    '''The view to create a new profile.'''
    model = BBProfile
    form_class = CreateProfileForm
    template_name = 'bloomboard/create_profile_form.html'
    def get_context_data(self, **kwargs):
        '''Add the user creation form to the context.'''
        context = super().get_context_data(**kwargs)
        context['user_form'] = UserCreationForm()
        return context
    def form_valid(self, form):
        '''Add the user and login the user after profile creation.'''
        user_form = UserCreationForm(self.request.POST)
        if user_form.is_valid():
            user = user_form.save()
            form.instance.user = user
            profile = form.save()
            login(self.request, user)
            return super().form_valid(form)
        else:
            return self.form_invalid(form)
    def get_success_url(self):
        '''Return the URL to display the profile page after creation.'''
        return reverse('show_profile')

# update profile view (login required )
class UpdateProfileView(UpdateView, LoginRequiredMixin):
    model = BBProfile
    form_class = UpdateProfileForm
    template_name = 'bloomboard/update_profile_form.html'
    def get_object(self):
        '''Get the object to update.'''
        return get_object_or_404(BBProfile, user=self.request.user)






##        POST VIEWS         ##






##        COMMENT VIEWS         ##
