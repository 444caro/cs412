# bloomboard/urls.py
from django.urls import path
from django.conf import settings
from . import views
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns=[
    path('', views.ShowAllProfilesView.as_view(), name='show_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', views.CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/update/', views.UpdateProfileView.as_view(), name='update_profile'),
    path('post/<int:pk>/delete/', views.DeletePostView.as_view(), name='delete_post'),
    path('post/<int:pk>/update/', views.UpdatePostView.as_view(), name='update_post'),
    path('show_all_flowers/', views.ShowAllFlowersView.as_view(), name='show_all_flowers'),
    path('flower/<int:pk>/', views.ShowFlowerView.as_view(), name='show_flower'),
    path('arrangements/', ShowAllArrangementsView.as_view(), name='show_all_arrangements'),
    path('arrangement/<int:pk>/', ShowArrangementView.as_view(), name='show_arrangement'),
    path('arrangement/<int:pk>/update/', UpdateArrangementView.as_view(), name='update_arrangement'),
    path('flowers/new/', CreateFlowerView.as_view(), name='create_flower'),
    path('vases/new/', CreateVaseView.as_view(), name='create_vase'),
    path('arrangements/new/', CreateArrangementView.as_view(), name='create_arrangement'),
    path('login/', auth_views.LoginView.as_view(template_name='bloomboard/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='bloomboard/logged_out.html'), name='logout'),
]