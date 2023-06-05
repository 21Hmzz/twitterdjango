from django.contrib import admin
from django.urls import path
from erttiwtBack import views
from erttiwtFront import views as viewsFront
from django.contrib.auth import views as auth_views

urlpatterns = [
   path('login/', auth_views.LoginView.as_view(template_name='erttiwtBack/login.html'), name='login'),
   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
   path('register/', views.register, name='register'),
   path('newTwitt/', views.newTwitt, name='newTwitt'),
   path('deletetweet/<int:idTwitt>', views.deletetweet, name='deletetweet'),
   path('like/<int:idTwitt>', views.like, name='like'),
   path('retweet/<int:idTwitt>', views.retweet, name='retweet'),
   path('follow/<int:idUser>', views.follow, name='follow'),
   path('editProfil/<str:username>', views.editProfil, name='editProfil'),
   path('saveProfil/', views.editProfilExecute, name='editProfilExecute'),
]