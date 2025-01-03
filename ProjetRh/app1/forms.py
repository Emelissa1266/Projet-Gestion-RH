from django import forms
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation, Conge, Contrat

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



class SalaireForm(forms.ModelForm):
    class Meta:
        model = Salaire
        fields = ['Employe_salaire', 'mois_annee', 'salaire_base', 'primes', 'heures_supplementaires', 'retenus', 'salaire_net']
        widgets = {
            'Employe_salaire': forms.Select(attrs={'class': 'form-control'}),
            'mois_annee': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'salaire_base': forms.NumberInput(attrs={'class': 'form-control'}),
            'primes': forms.NumberInput(attrs={'class': 'form-control'}),
            'heures_supplementaires': forms.NumberInput(attrs={'class': 'form-control'}),
            'retenus': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_net': forms.NumberInput(attrs={'class': 'form-control'}),
        }
       
class ContratForm(forms.ModelForm):
    class Meta:
        model = Contrat
        fields = ['Employe_Contrat', 'date_deb', 'date_fin', 'type_contrat', 'salaire_monsuel', 'salaire_quotidien', 'Employe_Contrat']
        widgets = {
            'Employe_Contrat': forms.Select(attrs={'class': 'form-control'}),
            'date_deb': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_contrat': forms.Select(attrs={'class': 'form-control'}),
            'salaire_monsuel': forms.NumberInput(attrs={'class': 'form-control'}),
            'salaire_quotidien': forms.NumberInput(attrs={'class': 'form-control'}),
            'Employe_Contrat': forms.Select(attrs={'class': 'form-control'}),
        }

class RecrutementForm(forms.ModelForm):
    class Meta:
        model = Recrutement
        fields = ['offre_emploi', 'description', 'status', 'date_debut', 'Condidat_Recrutement']
        widgets = {
            'offre_emploi': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Condidat_Recrutement': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['date_Evaluation', 'criteres', 'Resultat', 'Commentaire', 'Employe_Evaluation']
        widgets = {
            'date_Evaluation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'criteres': forms.TextInput(attrs={'class': 'form-control'}),
            'Resultat': forms.TextInput(attrs={'class': 'form-control'}),
            'Commentaire': forms.Textarea(attrs={'class': 'form-control'}),
            'Employe_Evaluation': forms.Select(attrs={'class': 'form-control'}),
        }