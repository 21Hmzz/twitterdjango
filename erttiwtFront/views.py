from django.shortcuts import render
from erttiwtFront.models import Twitt,Commentaire

# Create your views here.

def index(request):

    Twitts =  Twitt.objects.all()
    Commentaires = Commentaire.objects.all()

    return render(request, 'erttiwtFront/index.html', {'Tweets': Twitts, 'Commentaires': Commentaires})
