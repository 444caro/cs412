# bloomboard/models.py
# define the data objects that will be used in the bloomboard application
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

class Flower(models.Model):
    ''' A model to represent a flower.'''
    name = models.CharField(max_length=100) # name of the flower
    USE_TYPE_CHOICES = [('filler','Filler'),('focal','Focal'), ('greens','Greens')]
    use_type = models.CharField(max_length=10, choices=USE_TYPE_CHOICES)
    price_per_stem = models.DecimalField(max_digits=5, decimal_places=2)
    image_url = models.URLField(blank = False)
    
    def __str__(self):
        '''Return a string representation of the object.'''
        return f'{self.name}'

class Vase(models.Model):
    ''' A model to represent a vase.'''
    SIZE_CHOICES = [('small','Small'),('medium','Medium'), ('large','Large')]
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)    # size of the vase
    height = models.DecimalField(max_digits=5, decimal_places=2) # height of the vase in inches
    color = models.CharField(max_length=100) # color of the vase
    price = models.DecimalField(max_digits=5, decimal_places=2) # price of the vase
    
    def __str__(self):
        '''Return a string representation of the object.'''
        return f'{self.size} {self.color} Vase'





class BBProfile(models.Model):
    '''
    BBProfile is a model for the data attributes of individual bloomboard users.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.TextField(blank = False)
    lastName = models.TextField(blank = False)
    city = models.TextField(blank = False)
    image_url = models.URLField(blank = False)
    years_experience = models.IntegerField(blank = False)
    # `shop` (Foreign Key to Shop)
 
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.firstName} {self.lastName}'
      
class Post(models.Model):
    '''A model for Posts posted by users.'''
    profile = models.ForeignKey('BBProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=False)
    image = models.URLField(blank = False)
    # arrangement recipe, figure out later 

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Post by {self.profile} at {self.timestamp}'
    
class Comment(models.Model):
    '''A model for comments on posts.'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('BBProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    
    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Comment by {self.profile} at {self.timestamp}'

    

   
