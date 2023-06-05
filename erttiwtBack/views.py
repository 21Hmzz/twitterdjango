from django.shortcuts import render,redirect

from erttiwtFront.models import Twitt,Commentaire,Abonnements,TweetLike,TweetRetweet
from erttiwtBack.models import userProfilPictures
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from erttiwtBack.forms import TwittForm,UserRegisterForm,EditProfilForm 
from django.http import HttpResponse
from django.core import serializers
import json


# Create your views here.


def newTwitt(request):

    form = TwittForm(request.POST or None)
    if form.is_valid():
        tweet = Twitt()
        tweet.twitt = form.cleaned_data['twitt']
        tweet.user = request.user.id
        tweet.save()
        form = TwittForm()

    return redirect('/')

def deletetweet(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)
    twitt.delete()
    return redirect('/',{'message':'Tweet supprimé'})

def like(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)

    if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
        like = TweetLike.objects.get(user=request.user,tweet=idTwitt)
        like.delete()
        twitt = Twitt.objects.get(idTwitt=idTwitt)
        twitt.likes -= 1
        twitt.save()
        return redirect('/')
    else:
        like = TweetLike()
        like.user = request.user
        like.tweet = twitt
        like.save()
        twitt = Twitt.objects.get(idTwitt=idTwitt)
        twitt.likes += 1
        twitt.save()
        return redirect('/')

def retweet(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)
    if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
        retweet = TweetRetweet.objects.get(user=request.user,tweet=twitt)
        retweet.delete()
        twitt = Twitt.objects.get(idTwitt=idTwitt)
        twitt.retwitts -= 1
        twitt.save()
        return redirect('/')
    else:
        twitt.retwitts += 1
        twitt.save()
        retweet = TweetRetweet()
        retweet.user = request.user
        retweet.tweet = twitt
        retweet.save()
        return redirect('/')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            login(request,user)
            return redirect('/')
    else:
        form = UserRegisterForm()
    return render(request,'erttiwtBack/register.html',{'form':form})

def follow(request,idUser):
    user = User.objects.get(id=idUser)
    abonnement = Abonnements()
    abonnement.user = request.user.id
    abonnement.abonnement = user.id
    abonnement.save()
    return redirect('/')



def editProfil(request,username):
    form = EditProfilForm(
        instance=request.user,
    )
    if userProfilPictures.objects.filter(user=request.user.id).exists():
        image = userProfilPictures.objects.filter(user=request.user.id)
        image = image[0].profilPicture
    else:
        image = None
  
    
    return render(request, 'erttiwtFront/edit_profil.html', {'form': form,'image':image})

def editProfilExecute(request):
    if request.method == "POST":
        form = EditProfilForm(request.POST,request.FILES,instance=request.user)
        if form.is_valid():
            if request.FILES:
                if userProfilPictures.objects.filter(user=request.user.id).exists():
                    profilPicture = userProfilPictures.objects.get(user=request.user.id)
                    profilPicture.profilPicture = request.FILES['userpicture']
                    profilPicture.save()
                else:
                    profilPicture = userProfilPictures()
                    profilPicture.user = request.user.id
                    profilPicture.profilPicture = request.FILES['userpicture']
                    profilPicture.save()
            form.save()
            return redirect('/')
        
    else:
        form = EditProfilForm(instance=request.user)
    return render(request,'erttiwtFront/edit_profil.html',{'form':form})


def ajaxSearch(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(username__icontains=str(q))
        results = []
        for user in users:
            user_json = {}
            user_json['id'] = user.id
            user_json['label'] = user.username
            user_json['value'] = user.username
            if userProfilPictures.objects.filter(user=user.id).exists():
                image = userProfilPictures.objects.get(user=user.id)
                user_json['image'] = str(image.profilPicture)
            results.append(user_json)
        data = json.dumps(results)

    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

    
