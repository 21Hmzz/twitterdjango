from django.forms import ModelForm,Textarea
from erttiwtFront.models import Twitt,Commentaire
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class TwittForm(ModelForm):
    class Meta:
        model = Twitt
        fields = ['twitt']
        widgets = {
            'twitt': Textarea(attrs={'placeholder':'Quoi de neuf ?'}),
        }
class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(label="Prénom")
    last_name = forms.CharField(label="Nom")
    email = forms.EmailField(label="Email")
    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name','last_name','email')

class EditProfilForm(ModelForm):
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {
            'username':'Pseudo',
            'first_name': 'Prénom',
            'last_name': 'Nom',
            'email': 'Email',
        }