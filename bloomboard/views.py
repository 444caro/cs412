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
        # Initialize the flower usage formset if not already in kwargs
        context['form'] = self.get_form()
        FlowerUsageFormSet = modelformset_factory(FlowerUsage, form=FlowerUsageForm, extra=1, can_delete=True)
        if self.request.POST:
            context['flower_usage_formset'] = FlowerUsageFormSet(self.request.POST)
        else:
            context['flower_usage_formset'] = FlowerUsageFormSet(queryset=FlowerUsage.objects.none())
        return context

    def form_valid(self, form):
        """Handle valid form submissions."""
        context = self.get_context_data()
        flower_usage_formset = context['flower_usage_formset']

        if flower_usage_formset.is_valid():
            # Save the arrangement instance
            arrangement = form.save(commit=False)
            arrangement.profile = self.request.user.bbprofile  # Assuming a one-to-one relationship exists
            arrangement.save()

            # Save flower usages
            flower_usage_formset.instance = arrangement
            flower_usage_formset.save()

            return redirect(self.get_success_url())
        else:
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Handle invalid form submissions."""
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_success_url(self):
        """Redirect to the list of arrangements upon success."""
        return reverse('show_all_arrangements')

@login_required
def create_arrangement(request):
    FlowerUsageFormSet = modelformset_factory(FlowerUsage, form=FlowerUsageForm, extra=1, can_delete=True)

    if request.method == "POST":
        arrangement_form = CreateArrangementForm(request.POST)
        flower_usage_formset = FlowerUsageFormSet(request.POST, queryset=FlowerUsage.objects.none())

        if arrangement_form.is_valid() and flower_usage_formset.is_valid():
            # Save the arrangement
            arrangement = arrangement_form.save(commit=False)
            arrangement.profile = request.user.bbprofile
            arrangement.save()

            # Save flower usages
            for form in flower_usage_formset:
                if form.cleaned_data:  # Avoid empty forms
                    flower_usage = form.save(commit=False)
                    flower_usage.arrangement = arrangement
                    flower_usage.save()

            return redirect('show_all_arrangements')
    else:
        arrangement_form = CreateArrangementForm()
        flower_usage_formset = FlowerUsageFormSet(queryset=FlowerUsage.objects.none())

    return render(request, 'bloomboard/create_arrangement_form.html', {
        'form': arrangement_form,
        'flower_usage_formset': flower_usage_formset,
    })
    
    
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
