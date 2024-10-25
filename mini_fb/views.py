# mini_fb/views.py`
# define the views for the mini_fb app`
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from .models import *
from .forms import *

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
    template_name = 'mini_fb/create_status_form.html'

    def get_success_url(self):
        '''Return the URL to display the profile page after creation.'''
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})

    def form_valid(self, form):
        '''Add profile and handle file uploads.'''
        sm = form.save(commit=False)
        form.instance.profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        sm.save()
        
        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for file in files:
            image = Image(image_file=file, status_message=sm)
            image.save()
        
        return super().form_valid(form)
    
class UpdateProfileView(UpdateView):
    model = Profile
    form_class = UpdateProfileForm
    template_name = 'mini_fb/update_profile_form.html'
    
class DeleteStatusMessageView(DeleteView):
    model = StatusMessage
    template_name = 'mini_fb/delete_status_form.html'
    context_object_name = 'status_message'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
 
class UpdateStatusMessageView(UpdateView):
    model = StatusMessage
    fields = ['message']
    template_name = 'mini_fb/update_status_form.html'

    # Redirect to profile page after updating
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
class CreateFriendView(View):
    """View to handle adding a friend."""
    def dispatch(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs['pk'])
        other_profile = get_object_or_404(Profile, pk=self.kwargs['other_pk'])
        profile.add_friend(other_profile)
        return redirect('show_profile', pk=profile.pk)

class ShowFriendSuggestionsView(DetailView):
    model = Profile
    template_name = 'mini_fb/friend_suggestions.html'
    context_object_name = 'profile'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_suggestions'] = self.object.get_friend_suggestions()
        return context