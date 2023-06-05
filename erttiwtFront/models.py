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
    user = models.IntegerField()
    twitt = models.ForeignKey(Twitt, on_delete=models.CASCADE)
    def __str__(self):
        return self.commentaire + " Par : " + self.user

class Abonnements (models.Model):
    idAbonnements = models.AutoField(primary_key=True)
    user = models.IntegerField()
    abonnement = models.CharField(max_length=50)
    def __str__(self):
        return self.user + " suit " + self.abonnement

class TweetLike(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Twitt, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user + " like " + self.tweet

    class Meta:
        unique_together = ('user', 'tweet')
     

class TweetRetweet(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    tweet = models.ForeignKey(Twitt, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tweet')
    
    def __str__(self):
        return self.user + " retweet " + self.tweet