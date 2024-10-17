from django.urls import path
from django.conf import settings
from . import views
from .views import *


urlpatterns=[
    path('', RandomArticleView.as_view(), name='random'), 
    path('show_all', ShowAllView.as_view(), name='show_all'), 
    path('article/<int:pk>', ArticlePageView.as_view(), name='article'), 
    path('create_comment', CreateCommentView.as_view(), name='create_comment'), ### FIRST (WITHOUT PK)
    path('article/<int:pk>/create_comment', CreateCommentView.as_view(), name='create_comment'), ### NEW
    path('create_article', CreateArticleView.as_view(), name='create_article'),
    path('article/<int:pk>/update', UpdateArticleView.as_view(), name="update_article"),
    path('delete_comment/<int:pk>', DeleteCommentView.as_view(), name='delete_comment'), 
]