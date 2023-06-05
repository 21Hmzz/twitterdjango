from django.db import models

# Create your models here.
class userProfilPictures(models.Model):
    user = models.IntegerField(primary_key=True)
    profilPicture = models.ImageField(blank=True, null=True)
    def __str__(self):
        return "Photo de profil avec l'id : " + self.user.__str__()
