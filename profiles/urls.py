from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit_profile, name='edit_profile'),
    path('search/', views.search_profiles, name='search_profiles'),
    path('user/<int:pk>/', views.profile_detail, name='profile_detail'),
]
