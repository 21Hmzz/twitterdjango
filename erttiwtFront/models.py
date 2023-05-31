from django.db import models
from django import forms

# Create your models here.

class Twitt(models.Model):
    
    idTwitt = models.AutoField(primary_key=True)
    twitt = models.TextField(max_length=280,verbose_name="Quoi de neuf ?", help_text="280 caractères maximum")
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    likes = models.IntegerField(default=0)
    retwitts = models.IntegerField(default=0)
    def __str__(self):
        return self.twitt + " Par : " + self.user


class Commentaire(models.Model):
    idCommentaire = models.AutoField(primary_key=True)
    commentaire = models.CharField(max_length=280)
    date = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=50)
    twitt = models.ForeignKey(Twitt, on_delete=models.CASCADE)
    def __str__(self):
        return self.commentaire + " Par : " + self.user

