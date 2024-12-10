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
    ''' A model to represent a vase or arrangement container '''
    SIZE_CHOICES = [('small','Small'),('medium','Medium'), ('large','Large'), ('none','N/A')]  # none n/a is for arrangements that are not in a vase i.e., wrapped bouquets
    size = models.CharField(max_length=10, choices=SIZE_CHOICES)    # size of the vase
    height = models.DecimalField(max_digits=5, decimal_places=2, blank = True) # height of the vase in inches
    color = models.CharField(max_length=100, blank = True) # color of the vase
    price = models.DecimalField(max_digits=5, decimal_places=2) # price of the vase
    image_url = models.URLField(blank = True) # image of the vase
                                
    def __str__(self):
        '''Return a string representation of the object.'''
        return f'{self.height} inch tall {self.size} {self.color} Vase for ${self.price}'




class BBProfile(models.Model):
    '''
    BBProfile is a model for the data attributes of individual bloomboard users.
    '''
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    firstName = models.TextField(blank = False)
    lastName = models.TextField(blank = False)
    city = models.TextField(blank = False)
    image_url = models.URLField(blank = True)
    years_experience = models.IntegerField(blank = False)
    # `shop` (Foreign Key to Shop)
 
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.firstName} {self.lastName}'

    def get_absolute_url(self):
        '''Return the URL to display this BBProfile.'''
        return reverse('show_profile', kwargs={'pk':self.pk})
    
    def get_first_name(self):
        '''Return the first name of the user.'''
        return self.firstName
    
      
class Arrangement(models.Model):
    '''A model for arrangements created by users.'''
    profile = models.ForeignKey('BBProfile', on_delete=models.CASCADE)  # the user who created the arrangement
    occassion = models.TextField(blank=True) # occassion for the arrangement
    type = models.TextField(blank=True) # type of arrangement i.e., wrapped bouquet, handtied bouquet, centerpiece, vase, urn, funeral spray, etc.
    image = models.URLField(blank = False) # image of the arrangement
    vase = models.ForeignKey('Vase', on_delete=models.CASCADE, blank = True, null = True) # the vase or container for the arrangement, null if no vase
    

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Arrangement {self.pk} by {self.profile}'

    def get_all_flowers(self):
        '''Return all flowers and their quantities in the arrangement.'''
        return self.flower_usages.values('flower__name', 'quantity')

    def calculate_price(self):
        '''Calculate the total price of the arrangement.'''
        flower_cost = sum(
            usage.quantity * usage.flower.price_per_stem
            for usage in self.flower_usages.all()
        )
        if self.vase is None:
            return flower_cost
        return flower_cost + self.vase.price

class FlowerUsage(models.Model):
    '''A model to represent the usage of a flower in an arrangement.'''
    arrangement = models.ForeignKey('Arrangement', on_delete=models.CASCADE, related_name='flower_usages')
    flower = models.ForeignKey('Flower', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.arrangement}: {self.quantity} x {self.flower.name}'
    

      
      
      
      
class Post(models.Model):
    '''A model for Posts posted by users.'''
    profile = models.ForeignKey('BBProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    caption = models.TextField(blank=False)
    image = models.URLField(blank = False)
    arrangement = models.ForeignKey('Arrangement', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Post by {self.profile} at {self.timestamp}'
    class Meta:
        ordering = ['-timestamp']
    
class Comment(models.Model):
    '''A model for comments on posts.'''
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    profile = models.ForeignKey('BBProfile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    message = models.TextField(blank=False)
    
    def __str__(self):
        '''Return a string representation of the object.'''
        return f'Comment by {self.profile} at {self.timestamp}'

    

   
