from django.shortcuts import render,redirect

from erttiwtFront.models import Twitt,Commentaire,Abonnements,TweetLike,TweetRetweet
from erttiwtBack.models import userProfilPictures
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from erttiwtBack.forms import TwittForm,UserRegisterForm,EditProfilForm

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
    twitt.likes += 1
    twitt.save()
    like = TweetLike()
    like.user = request.user
    like.tweet = twitt
    like.save()
    return redirect('/')

def retweet(request,idTwitt):
    twitt = Twitt.objects.get(idTwitt=idTwitt)
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