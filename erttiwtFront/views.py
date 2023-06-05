from django.shortcuts import render,redirect
from erttiwtFront.models import Twitt,Commentaire,Abonnements,TweetLike,TweetRetweet
from erttiwtBack.models import userProfilPictures
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from erttiwtBack.forms import TwittForm

# Create your views here.

def index(request):

    Twitts =  Twitt.objects.all()
    all_users = User.objects.exclude(id=request.user.id)
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
        current_picture =  None
        
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
        if request.user.is_authenticated:
        
            if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
                twitt.likeParUser = True
            if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
                twitt.retweetParUser = True
        twitt.user = User.objects.get(id=twitt.user).username
        


    return render(request, 'erttiwtFront/index.html', {'Tweets': Twitts, 'users': all_users,'twittForm':twittForm,'current_user':current_user,'user_follow':user_follow,'user_follower':user_follower,'current_picture':current_picture})

def profil (request,username):
    if request.user.is_authenticated:

        userinfos = User.objects.get(username=username)
        user_follow = Abonnements.objects.filter(user=userinfos.id)
        user_follower = Abonnements.objects.filter(abonnement=userinfos.id)
        TweetLike_list = TweetLike.objects.filter(user=userinfos.id)
        TweetRetweet_list = TweetRetweet.objects.filter(user=userinfos.id)
        Twitts = Twitt.objects.filter(user=userinfos.id)
        


        
        if userProfilPictures.objects.filter(user=userinfos.id).exists():
            userinfos.picture = userProfilPictures.objects.get(user=userinfos.id).profilPicture
            
        
        for tweetRetweet in TweetRetweet_list:
            if Twitt.objects.filter(idTwitt=tweetRetweet.tweet.idTwitt).exists():
                tweetRetweet.tweet = Twitt.objects.get(idTwitt=tweetRetweet.tweet.idTwitt)
                if userProfilPictures.objects.filter(user=tweetRetweet.tweet.user).exists():
                    tweetRetweet.tweet.picture = userProfilPictures.objects.get(user=tweetRetweet.tweet.user).profilPicture
                tweetRetweet.tweet.likes = TweetLike.objects.filter(tweet=tweetRetweet.tweet.idTwitt).count()
                tweetRetweet.tweet.retwitts = TweetRetweet.objects.filter(tweet=tweetRetweet.tweet.idTwitt).count()
                tweetRetweet.tweet.commentaires = Commentaire.objects.filter(twitt=tweetRetweet.tweet.idTwitt)
                if request.user.is_authenticated:
                    if TweetLike.objects.filter(user=request.user,tweet=tweetRetweet.tweet).exists():
                        tweetRetweet.tweet.likeParUser = True
                    if TweetRetweet.objects.filter(user=request.user,tweet=tweetRetweet.tweet).exists():
                        tweetRetweet.tweet.retweetParUser = True
                tweetRetweet.tweet.user = User.objects.get(id=tweetRetweet.tweet.user).username
            
        for tweetLike in TweetLike_list:
            if Twitt.objects.filter(idTwitt=tweetLike.tweet.idTwitt).exists():
                tweetLike.tweet = Twitt.objects.get(idTwitt=tweetLike.tweet.idTwitt)
                if userProfilPictures.objects.filter(user=tweetLike.tweet.user).exists():
                    tweetLike.tweet.picture = userProfilPictures.objects.get(user=tweetLike.tweet.user).profilPicture
                tweetLike.tweet.likes = TweetLike.objects.filter(tweet=tweetLike.tweet.idTwitt).count()
                tweetLike.tweet.retwitts = TweetRetweet.objects.filter(tweet=tweetLike.tweet.idTwitt).count()
                tweetLike.tweet.commentaires = Commentaire.objects.filter(twitt=tweetLike.tweet.idTwitt)
                if request.user.is_authenticated:
                    if TweetLike.objects.filter(user=request.user,tweet=tweetLike.tweet).exists():
                        tweetLike.tweet.likeParUser = True
                    if TweetRetweet.objects.filter(user=request.user,tweet=tweetLike.tweet).exists():
                        tweetLike.tweet.retweetParUser = True
                tweetLike.tweet.user = User.objects.get(id=tweetLike.tweet.user).username
                    
            

        for twitt in Twitts:
            if request.user.is_authenticated:
                if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
                    twitt.likeParUser = True
                if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
                    twitt.retweetParUser = True

            twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)
            if userProfilPictures.objects.filter(user=twitt.user).exists():
                twitt.picture = userProfilPictures.objects.get(user=twitt.user).profilPicture
                twitt.user = User.objects.get(id=twitt.user).username
                twitt.likes = TweetLike.objects.filter(tweet=twitt.idTwitt).count()
                twitt.retwitts = TweetRetweet.objects.filter(tweet=twitt.idTwitt).count()
            

        paginator = Paginator(Twitts, 5)
        page = request.GET.get('page', 1)
        try:
            Twitts = paginator.page(page)
        except PageNotAnInteger:
            Twitts = paginator.page(1)
        except EmptyPage:
            Twitts = paginator.page(paginator.num_pages)

        

        return render(request, 'erttiwtFront/profil.html', {'userinfos': userinfos,'Tweets': Twitts,'user_follow':user_follow,'user_follower':user_follower,'TweetLike_list':TweetLike_list ,'TweetRetweet_list':TweetRetweet_list})
    else:
        return redirect('login')
