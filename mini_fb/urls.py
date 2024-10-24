from django.urls import path
from django.conf import settings
from . import views
from .views import *


urlpatterns=[
    path('', views.ShowAllProfilesView.as_view(), name='show_all_profiles'),
    path('profile/<int:pk>/', views.ShowProfilePageView.as_view(), name='show_profile'),
    path('create_profile/', CreateProfileView.as_view(), name='create_profile'),
    path('profile/<int:pk>/create_status/', CreateStatusMessageView.as_view(), name='create_status'),
    path('profile/<int:pk>/update/', UpdateProfileView.as_view(), name='update_profile'),
    path('status/<int:pk>/delete', views.DeleteStatusMessageView.as_view(), name='delete_status'),
    path('status/<int:pk>/update', views.UpdateStatusMessageView.as_view(), name='update_status'),
]