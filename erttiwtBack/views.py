from django.shortcuts import render,redirect

from erttiwtFront.models import Twitt,Commentaire
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from erttiwtBack.forms import TwittForm

# Create your views here.


def newTwitt(request):

    form = TwittForm(request.POST or None)
    if form.is_valid():
        tweet = Twitt()
        tweet.twitt = form.cleaned_data['twitt']
        tweet.user = request.user.username
        tweet.save()
        form = TwittForm()

    return redirect('/')

def deletetweet(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)
    twitt.delete()
    return redirect('/',{'message':'Tweet supprimé'})

def like(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)
    twitt.likes += 1
    twitt.save()
    return redirect('/')