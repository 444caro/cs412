# mini_fb/views.py`
# define the views for the mini_fb app`
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

# Create your views here.

# class based view 
class ShowAllProfilesView(ListView):
    '''the view to show all profiles'''
    model = Profile #the model to display
    template_name = 'mini_fb/show_all_profiles.html' #the template to use
    context_object_name = 'profiles' #model describes one profile, so we use the plural form for the context variable 
    
class ShowProfilePageView(DetailView, LoginRequiredMixin):
    """The view to show a profile page for a single user."""
    model = Profile  # The model to display
    template_name = 'mini_fb/show_profile.html'  # The template to use
    context_object_name = 'profile'  # The context variable name to access the profile in the template
    def get_object(self):
        '''Get the object to display.'''
        return get_object_or_404(Profile, user=self.request.user)

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect(reverse('login'))
        return super().get(request, *args, **kwargs)
    
class CreateProfileView(CreateView):
    '''The view to create a new profile.'''
    model = Profile
    form_class = CreateProfileForm
    template_name = 'mini_fb/create_profile_form.html'
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

class CreateStatusMessageView(CreateView, LoginRequiredMixin):
    '''The view to create a new status message.'''
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self):
        '''Return the URL to display the profile page after creation.'''
        return reverse('show_profile')

    def form_valid(self, form):
        '''Add profile and handle file uploads.'''
        form.instance.profile = self.request.user.profile
        sm = form.save(commit=False)
        sm.save()
        
        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()
        
        return super().form_valid(form)
    
class UpdateProfileView(UpdateView, LoginRequiredMixin):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    def get_object(self):
        '''Get the object to update.'''
        return get_object_or_404(Profile, user=self.request.user)
    
class DeleteStatusMessageView(DeleteView, LoginRequiredMixin):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile')
    def test_func(self):
        return self.request.user == self.get_object().profile.user
 
class UpdateStatusMessageView(UpdateView, LoginRequiredMixin):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    # Redirect to profile page after updating
    def get_success_url(self):
        return reverse('show_profile')
    
class CreateFriendView(View, LoginRequiredMixin):
    """View to handle adding a friend."""
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, user = request.user)
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile')

class ShowFriendSuggestionsView(DetailView, LoginRequiredMixin):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context
    
class ShowNewsFeedView(DetailView):
    model = Profile
    template_name = 'mini_fb/news_feed.html'
    context_object_name = 'profile'
    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['news_feed'] = self.object.get_news_feed()
        return context
    
class LoginUserView(LoginView):
    template_name = 'mini_fb/login.html'
class LogoutUserView(LogoutView):
    template_name = 'mini_fb/logged_out.html'