from django.contrib import admin
from django.urls import path, include
from erttiwtBack import views
from erttiwtFront import views as viewsFront
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='erttiwtBack/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(template_name='erttiwtBack/logout.html' ), name='logout'),
   path('register/', views.register, name='register'),
   path('newTwitt/', views.newTwitt, name='newTwitt'),
   path('deletetweet/<int:idTwitt>', views.deletetweet, name='deletetweet'),
   path('deletecomment/<int:idComment>', views.deletecomment, name='deletecomment'),
   path('like/<int:idTwitt>', views.like, name='like'),
   path('retweet/<int:idTwitt>', views.retweet, name='retweet'),
   path('follow/<int:idUser>', views.follow, name='follow'),
   path('comment/<int:idTwitt>', views.comment, name='comment'),
   path('editProfil/<str:username>', views.editProfil, name='editProfil'),
   path('saveProfil/', views.editProfilExecute, name='editProfilExecute'),
   path('search/', views.ajaxSearch, name='ajaxSearch'),
   path('setLightMode/', views.setLightMode, name='setLightMode'),
   path('setDarkMode/', views.setDarkMode, name='setDarkMode'),
]