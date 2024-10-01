# blog/models.py
# define the data objects that will be used in the blog application
from django.db import models

# Create your models here.
class Article(models.Model):
    '''Encapsulate the idea of one article by some author'''
    title = models.TextField(blank = False)  #false means it is required
    author = models.TextField(blank = False)
    text = models.TextField(blank = False)
    published = models.DateTimeField(auto_now = True)  #when object is created, it will automatically set the current time
    
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.title} by {self.author}'
