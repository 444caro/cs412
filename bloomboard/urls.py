# bloomboard/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('show_all_flowers/', views.ShowAllFlowersView.as_view(), name='show_all_flowers'),
    path('flower/<int:pk>/', views.ShowFlowerView.as_view(), name='show_flower'),
    path('login/', auth_views.LoginView.as_view(template_name='bloomboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bloomboard/logged_out.html'), name='logout'),
]