from django import forms
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation, Conge, Contrat, DemandeConge, DemandeAvanceSalaire

class loginForm(forms.Form):
    login = forms.CharField(label="Login", max_length=30, widget=forms.TextInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(label="Mot de passe", widget=forms.PasswordInput(attrs={"class": "form-control"}))
    mot_de_passe = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    
class SignupForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['Login', 'mot_de_passe', 'nom', 'prenom']
        widgets = {
            'Login': forms.EmailInput(attrs={
                'placeholder': 'Veuillez entrer votre email',
                'class': 'form-control',
            }),
            'mot_de_passe': forms.PasswordInput(attrs={
                'placeholder': 'Mot de passe',
                'class': 'form-control',
            }),
            'nom': forms.TextInput(attrs={
                'placeholder': 'Nom',
                'class': 'form-control',
            }),
            'prenom': forms.TextInput(attrs={
                'placeholder': 'Prénom',
                'class': 'form-control',
            }),
        }
        labels = {
            'Login': 'Nom d\'utilisateur',
            'mot_de_passe': 'Mot de passe',
            'nom': 'Nom',
            'prenom': 'Prénom',
        }




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
                  'Historique_professionnel', 'Service_Employe']
        widgets = {
            'Historique_professionnel': forms.Textarea(attrs={'class': 'form-control'}),
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
        fields = ['offre_emploi', 'description', 'status', 'date_debut']
        widgets = {
            'offre_emploi': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'status': forms.TextInput(attrs={'class': 'form-control'}),
            'date_debut': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
           
        }


class EvaluationForm(forms.ModelForm):
    class Meta:
        model = Evaluation
        fields = ['date_Evaluation', 'criteres', 'Resultat', 'Commentaire']
        widgets = {
            'date_Evaluation': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'criteres': forms.TextInput(attrs={'class': 'form-control'}),
            'Resultat': forms.TextInput(attrs={'class': 'form-control'}),
            'Commentaire': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class DemandeCongeForm(forms.ModelForm):
    class Meta:
        model = DemandeConge
        fields = ['date_deb', 'date_fin', 'type_conge', 'raison', 'commentaire']
        widgets = {
            'date_deb': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'type_conge': forms.Select(attrs={'class': 'form-control'}),
            'raison': forms.TextInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control'}),
            
        }


class DemandeAvanceSalaireForm(forms.ModelForm):
    class Meta:
        model = DemandeAvanceSalaire
        fields = ['Date_demande', 'Somme', 'commentaire']
        widgets = {
            'Date_demande': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'Sommet': forms.NumberInput(attrs={'class': 'form-control'}),
            'commentaire': forms.Textarea(attrs={'class': 'form-control'}),
            
        }

class EmployeProfileForm(forms.ModelForm):
    class Meta:
        model = Employe
        fields = [
            'nom', 
            'prenom', 
            'date_de_naissance', 
            'date_aumbauche', 
            'adresse', 
            'Historique_professionnel', 
            'Service_Employe', 
            'Competance_Employe', 
            'Employe_Formation',
            'photo_profil'
        ]
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'date_aumbauche': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'adresse': forms.TextInput(attrs={'class': 'form-control'}),
            'Historique_professionnel': forms.Textarea(attrs={'class': 'form-control'}),
        }

class CandidatProfileForm(forms.ModelForm):
    class Meta:
        model = Candidat
        fields = [
            'Nom', 
            'Prenom', 
            'Email',
            'CV',
        ]
        widgets = {
            'Nom': forms.TextInput(attrs={'class': 'form-control'}),
            'Prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'Email': forms.EmailInput(attrs={'class': 'form-control'}),
            'CV': forms.Textarea(attrs={'class': 'form-control'}),
        }
