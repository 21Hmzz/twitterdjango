from django.shortcuts import render,redirect
from erttiwtFront.models import Twitt,Commentaire,Abonnements,TweetLike,TweetRetweet,Messages,Conversation
from erttiwtBack.models import userProfilPictures,userCoverPictures
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from erttiwtBack.forms import TwittForm,CommentsForm,EditProfilForm,UserRegisterForm
from django.http import HttpResponseRedirect
from django.db.models import Q

# Create your views here.

def index(request):

    color_theme = request.COOKIES.get('mode')
    if color_theme == None:
        color_theme = 'dark'
    
    commentsForm = CommentsForm()

    commentaires = Commentaire.objects.all()

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
        for comment in twitt.commentaires:
            comment.username = User.objects.get(id=comment.user).username
            comment.first_name = User.objects.get(id=comment.user).first_name
            if userProfilPictures.objects.filter(user=comment.user).exists():
                comment.picture = userProfilPictures.objects.get(user=comment.user).profilPicture

        twitt.is_verified = User.objects.get(id=twitt.user).is_staff

        if userProfilPictures.objects.filter(user=twitt.user).exists():
            twitt.picture = userProfilPictures.objects.get(user=twitt.user).profilPicture
        if request.user.is_authenticated:
        
            if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
                twitt.likeParUser = True
            if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
                twitt.retweetParUser = True
        twitt.first_name = User.objects.get(id=twitt.user).first_name
        twitt.iduser = User.objects.get(id=twitt.user).id
        twitt.user = User.objects.get(id=twitt.user).username
        
        


    return render(request, 'erttiwtFront/index.html', {'commentaires':commentaires,'Tweets': Twitts, 'users': all_users,'twittForm':twittForm,'current_user':current_user,'user_follow':user_follow,'user_follower':user_follower,'current_picture':current_picture,'color_theme':color_theme,'commentsForm':commentsForm})

def profil (request,username):
    if request.user.is_authenticated:

        userinfos = User.objects.get(username=username)
        userinfos.is_verified = User.objects.get(username=username).is_staff
        user_follow = Abonnements.objects.filter(user=userinfos.id)
        user_follower = Abonnements.objects.filter(abonnement=userinfos.id)
        
        for user in user_follow:
            if userProfilPictures.objects.filter(user=user.abonnement).exists():
                user.picture = userProfilPictures.objects.get(user=user.abonnement).profilPicture
            user.username = User.objects.get(id=user.abonnement).username
            user.first_name = User.objects.get(id=user.abonnement).first_name
            if request.user.username == user.username:
                user.is_me = True
            else:
                user.is_me = False

        for user in user_follower:
            if userProfilPictures.objects.filter(user=user.user).exists():
                user.picture = userProfilPictures.objects.get(user=user.user).profilPicture
            user.username = User.objects.get(id=user.user).username
            user.first_name = User.objects.get(id=user.user).first_name
            user.is_verified = User.objects.get(id=user.user).is_staff
            if request.user.username == user.username:
                user.is_me = True
            else:
                user.is_me = False

            

        follow_you = Abonnements.objects.filter(abonnement=request.user.id,user=userinfos.id)
        if follow_you.exists():
            follow_you = True
        my_follow = Abonnements.objects.filter(user=request.user.id)
        for follow in my_follow:
            if Abonnements.objects.filter(user=request.user.id,abonnement=userinfos.id).exists():
                my_follow = True
            else:
                my_follow = False

        my_follower = Abonnements.objects.filter(abonnement=request.user.id)
        TweetLike_list = TweetLike.objects.filter(user=userinfos.id)
        TweetRetweet_list = TweetRetweet.objects.filter(user=userinfos.id)
        Twitts = Twitt.objects.filter(user=userinfos.id)
        


        
        if userProfilPictures.objects.filter(user=userinfos.id).exists():
            userinfos.picture = userProfilPictures.objects.get(user=userinfos.id).profilPicture
        if userCoverPictures.objects.filter(user=userinfos.id).exists():
            userinfos.cover = userCoverPictures.objects.get(user=userinfos.id).coverPicture
            
        
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
                tweetRetweet.tweet.user = User.objects.get(id=tweetRetweet.tweet.user)
            
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
                tweetLike.tweet.user = User.objects.get(id=tweetLike.tweet.user)
                    
            

        for twitt in Twitts:
            if request.user.is_authenticated:
                if TweetLike.objects.filter(user=request.user,tweet=twitt).exists():
                    twitt.likeParUser = True
                if TweetRetweet.objects.filter(user=request.user,tweet=twitt).exists():
                    twitt.retweetParUser = True

            twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)
            if userProfilPictures.objects.filter(user=twitt.user).exists():
                twitt.picture = userProfilPictures.objects.get(user=twitt.user).profilPicture
                twitt.user = User.objects.get(id=twitt.user)
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

        

        return render(request, 'erttiwtFront/profil.html', {'userinfos': userinfos,'Tweets': Twitts,'user_follow':user_follow,'user_follower':user_follower,'TweetLike_list':TweetLike_list ,'TweetRetweet_list':TweetRetweet_list,'my_follow':my_follow,'my_follower':my_follower,'follow_you':follow_you})
    else:
        return redirect('login')

def messages (request) :
    if request.user.is_authenticated:
        user = request.user
        userinfos = User.objects.get(id=user.id)
        userinfos.picture = userProfilPictures.objects.get(user=user.id).profilPicture
        userinfos.cover = userCoverPictures.objects.get(user=user.id).coverPicture
        userinfos.following = Abonnements.objects.filter(user=user.id).count()
        userinfos.followers = Abonnements.objects.filter(abonnement=user.id).count()
        userinfos.is_verified = User.objects.get(id=user.id).is_staff
        userinfos.username = User.objects.get(id=user.id).username
        userinfos.first_name = User.objects.get(id=user.id).first_name
        userinfos.date_joined = User.objects.get(id=user.id).date_joined
        userinfos.is_me = True
        userinfos.is_following = False
        userinfos.is_follower = False

        conversations = Conversation.objects.filter(Q(user1=user.id) | Q(user2=user.id))
        for conversation in conversations:
            lastmessage = Messages.objects.filter(idConversation=conversation.idConversation).last()
            conversation.lu = lastmessage.lu
            if lastmessage.user == user.id:
                conversation.lastmessage = "Vous : "+lastmessage.message
            else:
                conversation.lastmessage = lastmessage.message
            conversation.date = lastmessage.date
            destinataire = conversation.user1
            destinataire_user = User.objects.get(id=destinataire)
            conversation.username = destinataire_user.username
            conversation.first_name = destinataire_user.first_name
            if userProfilPictures.objects.filter(user=destinataire).exists():
                conversation.picture = userProfilPictures.objects.get(user=destinataire).profilPicture
           

       
        
        return render(request, 'erttiwtFront/message.html', {'userinfos': userinfos,'conversations':conversations})
            
    else:
        return redirect('login')

def messagesRead(request,idConversation):
    messageread = Messages.objects.filter(idConversation=idConversation)
    for message in messageread:
        message.lu = True
        message.save()
        if userProfilPictures.objects.filter(user=message.user).exists():
            message.picture = userProfilPictures.objects.get(user=message.user).profilPicture
        message.username = User.objects.get(id=message.user).username
        message.first_name = User.objects.get(id=message.user).first_name


    user = request.user
    userinfos = User.objects.get(id=user.id)
    userinfos.picture = userProfilPictures.objects.get(user=user.id).profilPicture
    userinfos.cover = userCoverPictures.objects.get(user=user.id).coverPicture
    userinfos.following = Abonnements.objects.filter(user=user.id).count()
    userinfos.followers = Abonnements.objects.filter(abonnement=user.id).count()
    userinfos.is_verified = User.objects.get(id=user.id).is_staff
    userinfos.username = User.objects.get(id=user.id).username
    userinfos.first_name = User.objects.get(id=user.id).first_name
    userinfos.date_joined = User.objects.get(id=user.id).date_joined
    userinfos.is_me = True
    userinfos.is_following = False
    userinfos.is_follower = False
    conversations = Conversation.objects.filter(Q(user1=user.id) | Q(user2=user.id))
    for conversation in conversations:
            lastmessage = Messages.objects.filter(idConversation=conversation.idConversation).last()
            conversation.lu = lastmessage.lu
            if lastmessage.user == user.id:
                conversation.lastmessage = "Vous : "+lastmessage.message
            else:
                conversation.lastmessage = lastmessage.message
            conversation.date = lastmessage.date
            destinataire = conversation.user1
            destinataire_user = User.objects.get(id=destinataire)
            conversation.username = destinataire_user.username
            conversation.first_name = destinataire_user.first_name
            if userProfilPictures.objects.filter(user=destinataire).exists():
                conversation.picture = userProfilPictures.objects.get(user=destinataire).profilPicture
           

    messages_list = Messages.objects.filter(Q(user=userinfos.id) | Q(destinataire=userinfos.id))
    for message in messages_list:
        if message.user == userinfos.id:
            message.lu = True
            message.save()
        if userProfilPictures.objects.filter(user=message.user).exists():
            message.picture = userProfilPictures.objects.get(user=message.user).profilPicture
        message.username = User.objects.get(id=message.user).username
        message.first_name = User.objects.get(id=message.user).first_name

    return render(request, 'erttiwtFront/message.html', {'userinfos': userinfos,'messages_list':messages_list,'messageread':messageread,'conversations':conversations})
