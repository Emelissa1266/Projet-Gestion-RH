from django import forms
from .models import Utilisateur, Candidat

class loginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))

class SignupForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['Login', 'mot_de_passe', 'nom', 'prenom']
        widgets = {
            'Login': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur', 'class': 'form-control'}),
            'mot_de_passe': forms.PasswordInput(attrs={'placeholder': 'Mot de passe', 'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'placeholder': 'Prénom', 'class': 'form-control'}),
        }
        labels = {
            'Login': 'Nom d\'utilisateur',
            'mot_de_passe': 'Mot de passe',
            'nom': 'Nom',
            'prenom': 'Prénom',
        }

    def clean_mot_de_passe(self):
        mot_de_passe = self.cleaned_data.get('mot_de_passe')
        if len(mot_de_passe) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return mot_de_passe