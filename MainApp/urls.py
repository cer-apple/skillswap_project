"""
URL patterns for MainApp
Maps URLs to views for the Campus SkillSwap application.
"""

from django.urls import path
from . import views

app_name = 'MainApp'  # Add app namespace for better URL organization

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Authentication
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Skill operations
    path('skill/create/', views.create_skill, name='create_skill'),
    path('skill/<int:pk>/', views.skill_detail, name='skill_detail'),
    path('skill/<int:pk>/edit/', views.update_skill, name='update_skill'),
    path('skill/<int:pk>/delete/', views.delete_skill, name='delete_skill'),

    # Reviews
    path('skill/<int:pk>/review/', views.add_review, name='add_review'),
    path('review/<int:pk>/delete/', views.delete_review, name='delete_review'),
    
    # User dashboard and profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
]
