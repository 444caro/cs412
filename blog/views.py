# blog/views.py`
# define the views for the blog app`
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
import random

# Create your views here.

# class based view 
class ShowAllView(ListView):
    '''the view to show all articles'''
    model = Article #the model to display
    template_name = 'blog/show_all.html' #the template to use
    context_object_name = 'articles' #model describes one article, so we use the plural form for the context variable 
    
class RandomArticleView(DetailView):
    '''Show the details for one article'''
    model = Article #the model to display
    template_name = 'blog/article.html' #the template to use
    context_object_name = 'article' #model describes one article, so we use the singular form for the context variable
    
    #pick one article at random
    def get_object(self):
        '''return one random article'''
        all_articles = Article.objects.all()
        return random.choice(all_articles)
    
class ArticlePageView(DetailView):
    '''Show the details for one article'''
    model = Article #the model to display
    template_name = 'blog/article.html' #the template to use
    context_object_name = 'article' #model describes one article, so we use the singular form for the context variable
