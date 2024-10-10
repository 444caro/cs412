# mini_fb/models.py
# define the data objects that will be used in the blog application
from django.db import models

# Create your models here.
class Profile(models.Model):
    '''
    Profile is a model for the data attributes of individual Facebook users.
    This Profile model will need to include the following data attributes: 
    first name, last name, city, email address, and a profile image url.
    '''
    firstName = models.TextField(blank = False)
    lastName = models.TextField(blank = False)
    city = models.TextField(blank = False)
    email = models.EmailField(blank = False)
    image_url = models.URLField(blank = False)
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.firstName} {self.lastName}'
    
class StatusMessage(models.Model):
    '''A model for status messages posted by users.'''
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Status by {self.profile} at {self.timestamp}'


