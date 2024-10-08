from django.urls import path
from django.conf import settings
from . import views
from .views import *


urlpatterns=[
    path('', RandomArticleView.as_view(), name = 'random'),
    path('show_all', ShowAllView.as_view(), name='show_all'),
    path('article/<int:pk>', ArticlePageView.as_view(), name='article')
]