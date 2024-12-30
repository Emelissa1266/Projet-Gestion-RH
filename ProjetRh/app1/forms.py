from django import forms
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation, Conge

class loginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
class SignupForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['Login', 'mot_de_passe', 'nom', 'prenom']
        widgets = {
            'Login': forms.EmailInput(attrs={'placeholder': 'Please enter your email', 'class': 'form-control'}),
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
        mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    def clean_mot_de_passe(self):
        mot_de_passe = self.cleaned_data.get('mot_de_passe')
        if len(mot_de_passe) < 8:
            raise forms.ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        return mot_de_passe

from django import forms
from .models import Utilisateur, Employe

class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['Login', 'mot_de_passe', 'nom', 'prenom', 'role']
        
        mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class EmployeForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = ['nom', 'prenom', 'date_de_naissance', 'date_aumbauche', 'adresse', 
                  'Historique_professionnel', 'Service_Employe', 'Competance_Employe', 
                  'Employe_Formation']
        widgets = {
            'Competance_Employe': forms.CheckboxSelectMultiple(),
            'Employe_Formation': forms.CheckboxSelectMultiple(),
        }

class CongeForm(forms.ModelForm):
    class Meta:
        model = Conge
        fields = ['date_deb', 'date_fin', 'type_conge', 'solde_conge', 'Employe_Conge']
        widgets = {
            'date_deb': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_conge': forms.Select(attrs={'class': 'form-control'}),
            'solde_conge': forms.NumberInput(attrs={'class': 'form-control'}),
            'Employe_Conge': forms.Select(attrs={'class': 'form-control'}),
        }