from django.contrib import admin
from django.urls import path
from erttiwtFront import views
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index),
    path('profil/<str:username>', views.profil),
    path('messages/<int:idConversation>', views.messagesRead),
    path('messages', views.messages, name='messages'),
    
]