from django.shortcuts import render
from erttiwtFront.models import Twitt,Commentaire
from django.contrib.auth.models import User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from erttiwtBack.forms import TwittForm

# Create your views here.

def index(request):

    Twitts =  Twitt.objects.all()
    all_users = User.objects.values()
    page = request.GET.get('page', 1)
    paginator = Paginator(all_users, 5)
    all_users = paginator.get_page(page)
    paginator = Paginator(Twitts, 5)
    current_user = request.user.username
    try:
        Twitts = paginator.page(page)
    except PageNotAnInteger:
        Twitts = paginator.page(1)
    except EmptyPage:
        Twitts = paginator.page(paginator.num_pages)
    twittForm = TwittForm()

    for twitt in Twitts:
        twitt.commentaires = Commentaire.objects.filter(twitt=twitt.idTwitt)
        


    return render(request, 'erttiwtFront/index.html', {'Tweets': Twitts, 'users': all_users,'twittForm':twittForm,'current_user':current_user})
