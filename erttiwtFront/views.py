from django.shortcuts import render
from erttiwtFront.models import Twitt,Commentaire,Abonnements,TweetLike,TweetRetweet
from erttiwtBack.models import userProfilPictures
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from erttiwtBack.forms import TwittForm

# Create your views here.

def index(request):

    Twitts =  Twitt.objects.all()
    all_users = User.objects.exclude(username=request.user.id)
    for user in all_users:
        if userProfilPictures.objects.filter(user=user.id).exists():
            user.picture = userProfilPictures.objects.get(user=user.id).profilPicture
        if Abonnements.objects.filter(user=request.user.id,abonnement=user.id).exists():
            user.follow = True
        else:
            user.follow = False
    
    

    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 5)
    all_users = paginator.get_page(page)
    paginator = Paginator(Twitts, 5)
    current_user = request.user.id
    if userProfilPictures.objects.filter(user=current_user).exists():
        current_picture = userProfilPictures.objects.get(user=current_user)
    else:
        current_picture =  "none"
        
    user_follow = Abonnements.objects.filter(user=current_user)
    user_follower = Abonnements.objects.filter(abonnement=current_user)
    try:
        Twitts = paginator.page(page)
    except PageNotAnInteger:
        Twitts = paginator.page(1)
    except EmptyPage:
        Twitts = paginator.page(paginator.num_pages)
    twittForm = TwittForm()

    for twitt in Twitts:
        twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)
        if userProfilPictures.objects.filter(user=twitt.user).exists():
            twitt.picture = userProfilPictures.objects.get(user=twitt.user).profilPicture
        if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
            twitt.likeParUser = True
        if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
            twitt.retweetParUser = True
        twitt.user = User.objects.get(id=twitt.user).username
        


    return render(request, 'erttiwtFront/index.html', {'Tweets': Twitts, 'users': all_users,'twittForm':twittForm,'current_user':current_user,'user_follow':user_follow,'user_follower':user_follower,'current_picture':current_picture})

def profil (request,username):

    userinfos = User.objects.get(username=username)
    Twitts = Twitt.objects.filter(user=userinfos)
    for twitt in Twitts:
        twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)

    paginator = Paginator(Twitts, 5)
    page = request.GET.get('page', 1)
    try:
        Twitts = paginator.page(page)
    except PageNotAnInteger:
        Twitts = paginator.page(1)
    except EmptyPage:
        Twitts = paginator.page(paginator.num_pages)

    

    return render(request, 'erttiwtFront/profil.html', {'userinfos': userinfos,'Tweets': Twitts})

