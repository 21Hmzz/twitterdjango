
from erttiwtBack.models import userProfilPictures
from erttiwtFront.models import Messages
from django.contrib.auth.models import User

def getColorTheme(request):
 
    return {'color_theme': request.COOKIES.get('mode', 'light')}

def getCurrentUser(request):
    return {'current_username': request.user}

def getProfilPicture(request):
    if request.user.is_authenticated:
        if userProfilPictures.objects.filter(user=request.user.id).exists():
            current_picture = userProfilPictures.objects.get(user=request.user.id)
        else:
            current_picture =  None
        return {'current_picturebase':current_picture}
    else:
        return {'current_picturebase':None}

def getMessages(request):
    if request.user.is_authenticated:
        if Messages.objects.filter(destinataire=request.user.id).exists():
            messages = Messages.objects.filter(destinataire=request.user.id)
            for message in messages:
               if userProfilPictures.objects.filter(user=message.user).exists():
                   message.picture = userProfilPictures.objects.get(user=message.user)
               message.first_name = User.objects.get(id=message.user).first_name
        else:
            messages = None
        return {'messages_tweet':messages}
    else:
        return {'messages':None}