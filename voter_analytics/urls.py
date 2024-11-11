# voter_analytics/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import *

urlpatterns=[
    path('', views.VoterListView.as_view(), name='voters'),
    path('voter/<int:pk>/', views.VoterDetailView.as_view(), name='voter'), 
    path('graphs/', views.VoterGraphsView.as_view(), name='graphs'),
]