from django.forms import ModelForm,Textarea
from erttiwtFront.models import Twitt,Commentaire

class TwittForm(ModelForm):
    class Meta:
        model = Twitt
        fields = ['twitt']
        widgets = {
            'twitt': Textarea(attrs={'placeholder':'Quoi de neuf ?'}),
        }
