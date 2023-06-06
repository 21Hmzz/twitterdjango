
from erttiwtBack.models import userProfilPictures
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