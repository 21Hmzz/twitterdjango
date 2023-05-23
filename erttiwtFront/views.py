from django.shortcuts import render
from erttiwtFront.models import Twitt,Commentaire

# Create your views here.

def index(request):

    Twitts =  Twitt.objects.all()
    for twitt in Twitts:
        twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)
        


    return render(request, 'erttiwtFront/index.html', {'Tweets': Twitts})
