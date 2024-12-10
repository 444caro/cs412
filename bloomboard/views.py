# bloomboard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView

##        FLOWER + ARRANGEMENT VIEWS         ##
# show all flowers
class ShowAllFlowersView(ListView):
    '''the view to show all flowers'''
    model = Flower #the model to display
    template_name = 'bloomboard/show_all_flowers.html' #the template to use
    context_object_name = 'flowers' #model describes one flower, so we use the plural form for the context variable

# show filtered flowers
class ShowFilteredFlowersView(ListView):
    '''the view to show all flowers that match a filter inputted by the user's form'''
    model = Flower #the model to display
    template_name = 'bloomboard/show_filtered_flowers.html' #the template to use
    context_object_name = 'flowers' #model describes one flower, so we use the plural form for the context variable
    
    def get_queryset(self):
        '''Filter the queryset based on the form data'''
        queryset = super().get_queryset()
        form = FlowerFilterForm(self.request.GET)
        if form.is_valid():
            queryset = form.filter_queryset(queryset)
        return queryset
    
    def get_context_data(self, **kwargs):
        '''Add the filter form to the context'''
        context = super().get_context_data(**kwargs)
        context['filter_form'] = FlowerFilterForm(self.request.GET)
        return context

# flower detail view 
class ShowFlowerView(DetailView):
    """The view to show a profile page for a single flower."""
    model = Flower  # The model to display
    template_name = 'bloomboard/show_flower.html'  # The template to use
    context_object_name = 'flower'  # The context variable name to access the flower in the template
    #note to self, add feature to see arrangements that use this flower, w the ability to click on the arrangement to see the arrangement post
    
    def get_absolute_url(self):
        '''Return the URL to display this flower.'''
        return reverse('show_flower', kwargs={'pk':self.pk})
    
    def get_arrangements(self):
        '''Return all arrangements that use this flower.'''
        flower_usages = FlowerUsage.objects.filter(flower=self.object)  # get all flower usages of this flower
        arrangements = [usage.arrangement for usage in flower_usages]  # get the arrangements from the flower usages
        return arrangements
    
    def get_context_data(self, **kwargs):
        '''Add the arrangements that use this flower to the context.'''
        context = super().get_context_data(**kwargs)
        context['arrangements'] = self.get_arrangements()
        return context

# arrangement list view
class ShowAllArrangementsView(ListView):
    '''the view to show all arrangements'''
    model = Arrangement #the model to display
    template_name = 'bloomboard/show_all_arrangements.html' #the template to use
    context_object_name = 'arrangements' #model describes one arrangement, so we use the plural form for the context variable


# arrangement detail view
class ShowArrangementView(DetailView):
    """The view to show a detail page for a single arrangement."""
    model = Arrangement  # The model to display
    template_name = 'bloomboard/show_arrangement.html'  # The template to use
    context_object_name = 'arrangement'  # The context variable name to access the arrangement in the template

    def get_context_data(self, **kwargs):
        """Add additional data to the context."""
        context = super().get_context_data(**kwargs)
        # Calculate total price of the arrangement
        arrangement = self.object
        context['total_price'] = arrangement.calculate_price()
        # Add flower usage data
        context['flower_usage'] = arrangement.get_all_flowers()
        return context

class CreateFlowerView(LoginRequiredMixin, CreateView):
    model = Flower
    form_class = CreateFlowerForm
    template_name = 'bloomboard/create_flower_form.html'

    def get_success_url(self):
        return reverse('show_all_flowers')
    
    
    
class CreateVaseView(LoginRequiredMixin, CreateView):
    model = Vase
    form_class = CreateVaseForm
    template_name = 'bloomboard/create_vase_form.html'

    def get_success_url(self):
        return reverse('show_all_arrangements')

class CreateArrangementView(LoginRequiredMixin, CreateView):
    model = Arrangement
    form_class = CreateArrangementForm
    template_name = 'bloomboard/create_arrangement_form.html'

    def get_context_data(self, **kwargs):
        """Provide context data for the template."""
        context = super().get_context_data(**kwargs)
        context['arrangement_form'] = context['form']
        context['profile'] = self.request.user.bbprofile
        # Use the pre-defined FlowerUsageFormSet
        if self.request.POST:
            context['flower_usage_formset'] = FlowerUsageFormSet(self.request.POST, instance = self.object)
        else:
            context['flower_usage_formset'] = FlowerUsageFormSet(instance = self.object)
        return context

    def form_valid(self, form):
        """Handle valid form submissions."""
        context = self.get_context_data()
        flower_usage_formset = context['flower_usage_formset']
        # Save the arrangement instance
        arrangement = form.save(commit=False)
        arrangement.profile = self.request.user.bbprofile  # Ensure profile is set
        arrangement.save()  # Save the arrangement to the database

        # Initialize the flower usage formset with the saved arrangement
        flower_usage_formset = FlowerUsageFormSet(self.request.POST, instance=arrangement)

        if flower_usage_formset.is_valid():
            # Save flower usages
            flower_usages = flower_usage_formset.save(commit=False)
            for flower_usage in flower_usages:
                flower_usage.arrangement = arrangement
                flower_usage.save()
            # Save any remaining changes in the formset, e.g., marked-for-deletion items
            flower_usage_formset.save()
            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submissions."""
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        """Redirect to the detail view of the arrangment upon success."""
        return reverse('show_all_arrangements')

class UpdateArrangementView(LoginRequiredMixin, UpdateView):
    '''The view to update an arrangement and add more flowers to it.'''
    model = Arrangement
    form_class = UpdateArrangementForm
    template_name = 'bloomboard/update_arrangement_form.html'

    def get_context_data(self, **kwargs):
        """Provide context data for the template."""
        context = super().get_context_data(**kwargs)
        context['flower_usage_formset'] = FlowerUsageFormSet(
            self.request.POST or None, 
            instance=self.object
        )

        return context

    def form_valid(self, form):
        """Handle valid form submissions."""
        context = self.get_context_data()
        flower_usage_formset = context['flower_usage_formset']
        print("POST data:", self.request.POST) # Debugging
        if flower_usage_formset.is_valid():
            arrangement = form.save(commit=False)
            arrangement.profile = self.request.user.bbprofile  # Assuming this field exists
            arrangement.save()

            # Save flower usages
            flower_usage_formset.instance = arrangement
            flower_usage_formset.save()

            return redirect(self.get_success_url())
        else:
            # Debugging validation errors
            print("Formset errors:", flower_usage_formset.errors)
            print("Non-form errors:", flower_usage_formset.non_form_errors())
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submissions."""
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)

    def get_success_url(self):
        """Redirect to the list of arrangements upon success."""
        return reverse('show_all_arrangements')
    
    
    
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

    def get_context_data(self, **kwargs):
        """Add the profile's posts to the context."""
        # Call the superclass's method to get the existing context
        context = super().get_context_data(**kwargs)
        
        # Fetch the profile instance using the primary key (pk) from the URL
        bbprofile = self.get_object()
        
        # Get all posts by this user, ordered by creation date (reverse chronological)
        posts = Post.objects.filter(profile=bbprofile).order_by('-timestamp') 

        # Add the posts to the context dictionary
        context['posts'] = posts
        
        return context
    
    def get_absolute_url(self):
        '''Return the URL to display this BBProfile.'''
        return reverse('show_profile', kwargs={'pk':self.pk})


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
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = BBProfile
    form_class = UpdateProfileForm
    template_name = 'bloomboard/update_profile_form.html'
    def get_object(self):
        '''Get the object to update.'''
        return get_object_or_404(BBProfile, user=self.request.user)


##        POST VIEWS         ##
class CreatePostView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = CreatePostForm
    template_name = 'bloomboard/create_post_form.html'

    def form_valid(self, form):
        form.instance.profile = self.request.user.bbprofile
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.request.user.bbprofile.pk})

class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'bloomboard/delete_post_form.html'
    context_object_name = 'post'

    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    def test_func(self):
        return self.request.user == self.get_object().profile.user

 
class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = UpdatePostForm
    template_name = 'bloomboard/update_post_form.html'

    # Redirect to profile page after updating
    def get_success_url(self):
        return reverse('show_profile', kwargs={'pk': self.object.profile.pk})
    
    def test_func(self):
        """Ensure only the post owner can update the post."""
        return self.request.user == self.get_object().profile.user




##        COMMENT VIEWS         ##
