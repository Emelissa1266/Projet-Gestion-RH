from django import forms
from .models import Utilisateur

class AuthentificationForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SignupForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['Login', 'mot_de_passe']
        widgets = {
            'mot_de_passe': forms.PasswordInput(attrs={'placeholder': 'Mot de passe'}),
        }
        labels = {
            'Login': 'Nom d\'utilisateur',
            'mot_de_passe': 'Mot de passe',
        }