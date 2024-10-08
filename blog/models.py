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
    image_url = models.URLField(blank=True)   #true means optional field
    
    def __str__(self):
        '''return a string representation of the object'''
        return f'{self.title} by {self.author}'

class Comment(models.Model):
    '''Encapsulate the idea of a Comment on an Article.'''
    
    # data attributes of a Comment:
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    author = models.TextField(blank=False)
    text = models.TextField(blank=False)
    published = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        '''Return a string representation of this Comment object.'''
        return f'{self.text}'
    
    def get_comments(self):
        '''Return all of the comments about this article.'''
        comments = Comment.objects.filter(article=self)
        return comments