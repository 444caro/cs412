# blog/views.py`
# define the views for the blog app`
from django.shortcuts import render
from django.views.generic import ListView
from .models import *

# Create your views here.

# class based view 
class ShowAllView(ListView):
    '''the view to show all articles'''
    model = Article #the model to display
    template_name = 'blog/show_all.html' #the template to use
    context_object_name = 'articles' #model describes one article, so we use the plural form for the context variable 
    
