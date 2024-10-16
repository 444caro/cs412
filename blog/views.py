# blog/views.py`
# define the views for the blog app`
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import *
import random
from django.views.generic.edit import CreateView
from .forms import CreateCommentForm
from django.urls import reverse
from typing import Any
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

class CreateCommentView(CreateView):
    '''A view to create a new comment and save it to the database.'''
    form_class = CreateCommentForm
    template_name = "blog/create_comment_form.html"
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        '''
        Build the dict of context data for this view.
        '''
        # superclass context data
        context = super().get_context_data(**kwargs)
        # find the pk from the URL
        pk = self.kwargs['pk']
        # find the corresponding article
        article = Article.objects.get(pk=pk)
        # add article to context data
        context['article'] = article
        return context
    def form_valid(self, form):
        '''
        Handle the form submission. We need to set the foreign key by 
        attaching the Article to the Comment object.
        We can find the article PK in the URL (self.kwargs).
        '''
        print(form.cleaned_data)
        article = Article.objects.get(pk=self.kwargs['pk'])
        # print(article)
        form.instance.article = article
        return super().form_valid(form)
    
    ## show how the reverse function uses the urls.py to find the URL pattern
    def get_success_url(self) -> str:
        '''Return the URL to redirect to after successfully submitting form.'''
        #return reverse('show_all')
        return reverse('article', kwargs={'pk': self.kwargs['pk']})