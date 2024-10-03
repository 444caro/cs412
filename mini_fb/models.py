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


