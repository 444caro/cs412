# mini_fb/models.py
# define the data objects that will be used in the blog application
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    '''
    Profile is a model for the data attributes of individual Facebook users.
    This Profile model will need to include the following data attributes: 
    first name, last name, city, email address, and a profile image url.
    '''
    #user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    firstName = models.TextField(blank = False)
    lastName = models.TextField(blank = False)
    city = models.TextField(blank = False)
    email = models.EmailField(blank = False)
    image_url = models.URLField(blank = False)

    
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.firstName} {self.lastName}'
    def get_absolute_url(self):
        '''Return the URL to display the profile.'''
        return reverse('show_profile', kwargs={'pk': self.pk})
    
    def get_status_messages(self):
        '''Return all status messages for this profile.'''
        return self.statusmessage_set.all().order_by('-timestamp')
    
    def get_friends(self):
        """Return a list of all friends for this profile."""
        friends = Friend.objects.filter(models.Q(profile1=self) | models.Q(profile2=self))
        friends_list = [friend.profile1 if friend.profile2 == self else friend.profile2 for friend in friends]
        return friends_list
    def add_friend(self, other):
        """Add a friend to the profile, avoiding duplicates and self-friending."""
        if self != other:
            if not Friend.objects.filter(models.Q(profile1=self, profile2=other) | models.Q(profile1=other, profile2=self)).exists():
                Friend.objects.create(profile1=self, profile2=other)
    def get_friend_suggestions(self):
        """Return a list of Profiles that are not currently friends."""
        friends = self.get_friends()
        suggestions = Profile.objects.exclude(pk=self.pk).exclude(pk__in=[friend.pk for friend in friends])
        return suggestions
    
    def get_news_feed(self):
        """Return a queryset of all status messages by the profile and their friends."""
        friends = self.get_friends()
        return StatusMessage.objects.filter(profile__in=friends + [self]).order_by('-timestamp')

    
class StatusMessage(models.Model):
    '''A model for status messages posted by users.'''
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Status by {self.profile} at {self.timestamp}'
    def get_images(self):
        '''Return all images associated with this status message.'''
        return self.image_set.all()
    
class Image(models.Model):
    image_file = models.ImageField(upload_to='media/')
    status_message = models.ForeignKey('StatusMessage', on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Image for {self.status_message} uploaded at {self.uploaded_at}'
    
class Friend(models.Model):
    profile1 = models.ForeignKey('Profile', related_name='profile1', on_delete=models.CASCADE)
    profile2 = models.ForeignKey('Profile', related_name='profile2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.profile1} & {self.profile2}'
    

