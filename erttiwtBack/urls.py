from django.contrib import admin
from django.urls import path
from erttiwtBack import views
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='erttiwtBack/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('newTwitt/', views.newTwitt, name='newTwitt'),
   path('deletetweet/<int:idTwitt>', views.deletetweet, name='deletetweet'),
   path('like/<int:idTwitt>', views.like, name='like'),
]