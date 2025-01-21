from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import loginForm, SignupForm,EmployeProfileForm,CandidatProfileForm  ,EmployeForm ,UtilisateurForm ,CongeForm, SalaireForm, ContratForm, RecrutementForm, EvaluationForm, DemandeCongeForm, DemandeAvanceSalaireForm
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation ,Conge ,DemandeConge, DemandeAvanceSalaire, Contrat, ArchiveContrat
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
import pandas as pd 
import plotly.express as px
from datetime import datetime
from plotly.offline import plot
from django.shortcuts import render



def home_candidat(request):
    return render(request, 'home_candidat.html')

# Vue pour l'inscription
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Créer un utilisateur sans l'enregistrer pour ajouter des champs personnalisés
            utilisateur = form.save(commit=False)
            utilisateur.Login = form.cleaned_data['Login']
            
            # Hacher le mot de passe avant de le sauvegarder
            utilisateur.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])
            utilisateur.role = 'candidate'  # Rôle par défaut
            utilisateur.save()

            # Créer un objet Candidat lié à cet utilisateur
            Candidat.objects.create(
                Nom=utilisateur.nom,
                Prenom=utilisateur.prenom,
                Utilisateur_Condidat=utilisateur,
                Email=utilisateur.Login,  # Utiliser l'email comme identifiant
                Etat_condidature="en attente"  # État par défaut
            )

            # Rediriger vers la page de connexion après inscription
            return redirect('connexion')
    else:
        # Formulaire vide pour une requête GET
        form = SignupForm()

    # Rendre le template avec le formulaire
    return render(request, 'signup.html', {'form': form})




#Fonction pour l'authentification
def RedirectionVersPage(request):
    if request.method == 'POST':
        form = loginForm(request.POST) # Récupérer les données du formulaire
        if form.is_valid():
            Login = form.cleaned_data["login"]
            Mot_de_passe = form.cleaned_data["mot_de_passe"]
            try:
                utilisateur = Utilisateur.objects.get(Login=Login)
                if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'admin': # Si le login et le mot de passe sont corrects et le rôle est "admin"
                  return redirect('acceuil_arh')
                else:
                     if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'manager': # Si le login et le mot de passe sont corrects et le rôle est "manager"
                       return render(request, 'AcceuilMan.html')
                     else:
                         if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'employee': # Si le login et le mot de passe sont corrects et le rôle est "employee"
                            return render(request, 'AcceuilEmp.html', {'utilisateur': utilisateur.id})
                         else:
                              if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'candidate': # Si le login et le mot de passe sont corrects et le rôle est "candidate"
                                 return redirect('acceuil-cand', utilisateur.id)
                              else: # Si le mot de passe est incorrect
                                    form.add_error('login', "Login ou mot de passe incorrect !")
                                    msg = "Login ou mot de passe incorrect !"
                                    return render(request, "login.html", {"form": form, "msg": msg})
            except Utilisateur.DoesNotExist: # Si l'utilisateur n'existe pas
                form.add_error('login', "Login ou mot de passe incorrect !")
                msg = "Login ou mot de passe incorrect !"
                return render(request, "login.html", {"form": form, "msg": msg})
    else:
        form = loginForm() # Créer un formulaire vide si c'est une requête GET
        return render(request, "login.html", {"form": form})
    


def liste_employes(request):
    employes = Employe.objects.select_related('Employe_Utilisateur').all()
    return render(request, 'liste_employes.html', {'employes': employes})

def ajouter_employe(request):
    if request.method == "POST":
        utilisateur_form = UtilisateurForm(request.POST)
        employe_form = EmployeForm(request.POST)

        if utilisateur_form.is_valid() and employe_form.is_valid():
            # Sauvegarde les informations utilisateur
            utilisateur = utilisateur_form.save()

            # Associe l'utilisateur à l'employé et sauvegarde les informations employé
            employe = employe_form.save(commit=False)
            employe.Employe_Utilisateur = utilisateur
            employe.save()
            employe_form.save_m2m()  # Sauvegarde les relations ManyToMany

            messages.success(request, "Employé ajouté avec succès !")
            return redirect('liste_employes')  # Redirige vers la liste des employés
    else:
        utilisateur_form = UtilisateurForm()
        employe_form = EmployeForm()

    return render(request, 'ajouter_employe.html', {
        'utilisateur_form': utilisateur_form,
        'employe_form': employe_form,
    })


def modifier_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    utilisateur = employe.Employe_Utilisateur  # Récupère l'utilisateur lié à l'employé

    if request.method == 'POST':
        employe_form = EmployeForm(request.POST, instance=employe)
        utilisateur_form = UtilisateurForm(request.POST, instance=utilisateur)

        if employe_form.is_valid() and utilisateur_form.is_valid():
            employe_form.save()
            utilisateur_form.save()
            messages.success(request, "Les informations de l'employé ont été mises à jour avec succès.")
            return redirect('liste_employes')
    else:                           
        employe_form = EmployeForm(instance=employe)
        utilisateur_form = UtilisateurForm(instance=utilisateur)

    return render(request, 'modifier_employe.html', {
        'employe_form': employe_form,
        'utilisateur_form': utilisateur_form,
        'employe': employe,
    })

def supprimer_employe(request, employe_id):
    if request.method == "POST":
        employe = get_object_or_404(Employe, id=employe_id)
        utilisateur = employe.Employe_Utilisateur  # Get the associated user
        employe.delete()  # Delete the employee
        
        # Now delete the associated user
        utilisateur.delete()
        
        return redirect('liste_employes')  # Redirect to the list of employees
    return redirect('liste_employes')  # If the request is not POST, just redirect back to the list


# Vue pour afficher les détails d'un employé
def detail_employe(request, employe_id):
    employe = get_object_or_404(Employe, id=employe_id)
    return render(request, 'Fiche_employe.html', {'employe': employe})


# Vue pour la liste des évaluations pour l'accès ARH
def liste_evaluations(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'liste_evaluations.html', {'evaluations': evaluations})

# Vue pour afficher le rapport d'une évaluation
def rapport_evaluation(request, evaluation_id):
    evaluation = get_object_or_404(Evaluation, id=evaluation_id)
    return render(request, 'rapport_evaluation.html', {'evaluation': evaluation , 'date': evaluation.date_Evaluation})

# Vue pour supprimer une évaluation
def supprimer_evaluation(request, evaluation_id):
    if request.method == "POST":
        evaluation = get_object_or_404(Evaluation, id=evaluation_id)
        evaluation.delete()  # Delete the evaluation
        return redirect('liste_evaluations')  # Redirect to the list of evaluations
    return redirect('liste_evaluations')  # If the request is not POST, just redirect back to the list

# Vue pour la liste des congés
def liste_conges(request):
    conges = Conge.objects.all()

    # Récupérer les congés dont la date de fin est égale à la date d'aujourd'hui
    today = timezone.now().date()
    conges_fin_aujourdhui = conges.filter(date_fin=today)

    # Envoyer une notification à chaque employé concerné
    for conge in conges_fin_aujourdhui:
        employe = conge.Employe_Conge
        messages.info(request, f'Bonjour {employe.prenom}, votre congé se termine aujourd\'hui. Nous vous attendons demain au travail.')

    return render(request, 'liste_conges.html', {'conges': conges})

# Vue pour ajouter un nouveau congé
def ajouter_conge(request):
    if request.method == 'POST':
        form = CongeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_conges')  # Redirection vers la liste des congés après ajout
    else:
        form = CongeForm()

    return render(request, 'ajouter_conge.html', {'form': form})

def supprimer_conge(request, conge_id):
    if request.method == "POST":
        conge = get_object_or_404(Conge, id=conge_id)
        conge.delete()  # supprimer le congé
        return redirect('liste_conges')  # Rediriger vers la liste des congés
    return redirect('liste_conges') # If the request is not POST, just redirect back to the list



def liste_demandes_conges(request):
    demandes_conges = DemandeConge.objects.all()
    return render(request, 'liste_demande.html', {'demandes_conges': demandes_conges})


@csrf_exempt
def accepter_demande_conge(request, demande_id):
            demande = DemandeConge.objects.get(id=demande_id)
            # Create a new Conge object
            Conge.objects.create(
                Employe_Conge=demande.employe,
                date_deb=demande.date_deb,
                date_fin=demande.date_fin,
                type_conge=demande.type_conge,
                solde_conge=1000,
            )
            demande.statut = "Approuvé"
            demande.save()
            return redirect('liste_demande_conge')

# Vue pour refuser une demande de congé
@csrf_exempt
def refuser_demande_conge(request, demande_id):
    if request.method == 'POST':
            demande = DemandeConge.objects.get(id=demande_id)
            demande.statut = "Rejeté",
            demande.save()
    return redirect('liste_demande_conge')


def liste_salaires(request):
    salaires = Salaire.objects.all()
    return render(request, 'liste_salaires_ARH.html', {'salaires': salaires})


def ajouter_salaire(request):
    if request.method == 'POST':
        form = SalaireForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_salaires')  # Redirection vers la liste des salaires après ajout
    else:
        form = SalaireForm()

    return render(request, 'ajouter_salaire.html', {'form': form})

def supprimer_salaire(request, salaire_id):
    if request.method == "POST":
        salaire = get_object_or_404(Salaire, id=salaire_id)
        salaire.delete()  # supprimer le salaire
        return redirect('liste_salaires')  # Rediriger vers la liste des salaires
    return redirect('liste_salaires') # If the request is not POST, just redirect back to the list

def fiche_paie(request, salaire_id):
    salaire = get_object_or_404(Salaire, id=salaire_id)
    # Rechercher l'employé correspondant
    return render(request, 'Fiche_paie_ARH.html', {'salaire': salaire, 'date': salaire.mois_annee})

def liste_demande_avance_salaire(request):
    demandes_avance = DemandeAvanceSalaire.objects.all()
    return render(request, 'liste_demande_avance_salaire.html', { 'demandes_avance': demandes_avance})

def accepter_demande_avance_salaire(request, demande_id):
    demande = DemandeAvanceSalaire.objects.get(id=demande_id)
    Salaire.objects.create(
        Employe_salaire=demande.Employe_demande,
        mois_annee=demande.Date_demande,
        salaire_base=demande.Somme,
        primes=0,
        heures_supplementaires=0,
        retenus=0,
        salaire_net=demande.Somme,
    )
    # Update the status of the request
    demande.statut = "Approuvé"
    demande.save()  
    return redirect('avance_salaire')

def refuser_demande_avance_salaire(request, demande_id):
    demande = DemandeAvanceSalaire.objects.get(id=demande_id)
    demande.statut = "Rejeté"
    demande.save()  
    return redirect('avance_salaire')

def liste_contrats(request):
    contrats = Contrat.objects.all()
    return render(request, 'liste_contrats.html', {'contrats': contrats})

# Vue pour ajouter un nouveau contrat
def ajouter_contrat(request):
    if request.method == 'POST':
        form = ContratForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')  # Redirection vers la liste des contrats après ajout
    else:
        form = ContratForm()

    return render(request, 'ajouter_contrat.html', {'form': form})

def modifier_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)

    if request.method == 'POST': # Si la requête est de type POST
        # Récupérer les données du formulaire et les associer à l'instance du contrat
        form = ContratForm(request.POST, instance=contrat)
        if form.is_valid():
            form.save()
            return redirect('liste_contrats')  # Redirection vers la liste des contrats après modification
    else: # Si la requête est de type GET
        # Créer un formulaire pré-rempli avec les données du contrat
        form = ContratForm(instance=contrat)

    return render(request, 'modifier_contrat.html', {'contrat_form': form, 'contrat': contrat})

def consulter_contrat(request, contrat_id):
    contrat = get_object_or_404(Contrat, id=contrat_id)
    return render(request, 'consulter_contrat.html', {'contrat': contrat, 'date': contrat.date_deb})


def liste_archives_contrats(request):
    contrats = ArchiveContrat.objects.all()
    return render(request, 'Archives_contrat.html', {'contrats': contrats})


def supprimer_contrat(request, contrat_id):
    if request.method == "POST":
        contrat = get_object_or_404(Contrat, id=contrat_id)
        # Archiver le contrat
        ArchiveContrat.objects.create(
            Employe =contrat.Employe_Contrat,
            date_deb=contrat.date_deb,
            date_fin=contrat.date_fin,
            type_contrat=contrat.type_contrat,
            salaire_monsuel=contrat.salaire_monsuel,
            salaire_quotidien=contrat.salaire_quotidien,
            date_archive=timezone.now()
        )
        contrat.delete()  # Supprimer le contrat
        return redirect('liste_contrats')  # Rediriger vers la liste des contrats
    return redirect('liste_contrats')  # Si la requête n'est pas POST, rediriger vers la liste


# Vue pour la liste des recrutements
def liste_recrutements(request):
    recrutements = Recrutement.objects.all()
    return render(request, 'liste_recrutements.html', {'recrutements': recrutements})

# Vue pour modifier un recrutement
def modifier_recrutement(request, recrutement_id):
    recrutement = get_object_or_404(Recrutement, id=recrutement_id)
    if request.method == 'POST':
        form = RecrutementForm(request.POST, instance=recrutement)
        if form.is_valid():
            form.save()
            return redirect('liste_recrutements')  # Redirection vers la liste des recrutements après modification
    else:
        form = RecrutementForm(instance=recrutement)

    return render(request, 'modifier_recrutement.html', {'recrutement_form': form, 'recrutement': recrutement})

# Vue pour afficher les détails d'un recrutement
def details_recrutement(request, recrutement_id):
    recrutement = get_object_or_404(Recrutement, id=recrutement_id)
    return render(request, 'details_recrutement.html', {'recrutement': recrutement})

# Vue pour supprimer un recrutement
def supprimer_recrutement(request, recrutement_id):
    if request.method == "POST":
        recrutement = get_object_or_404(Recrutement, id=recrutement_id)
        recrutement.delete()  # Supprimer le recrutement
        return redirect('liste_recrutements')  # Rediriger vers la liste des recrutements
    return redirect('liste_recrutements')  # Si la requête n'est pas POST, rediriger vers la liste

# Vue pour ajouter un nouveau recrutement
def ajouter_recrutement(request):
    if request.method == 'POST':
        form = RecrutementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('liste_recrutements')  # Redirection vers la liste des recrutements après ajout
    else:
        form = RecrutementForm()

    return render(request, 'ajouter_recrutement.html', {'recrutement_form': form})

# Vue pour afficher la liste des candidats pour un recrutement
def liste_candidats(request, recrutement_id):
    recrutement = get_object_or_404(Recrutement, id=recrutement_id)
    candidats = recrutement.Condidat_Recrutement.all()
    return render(request, 'liste_candidats.html', {'candidats': candidats, 'recrutement': recrutement})

# Vue pour afficher les détails d'un candidat
def details_candidat(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    return render(request, 'details_candidat.html', {'candidat': candidat})

# Vue pour refuser un candidat
def refuser_candidat(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    candidat.Etat_condidature = "Rejeté"
    id_recrutement = candidat.Rcrt_cond.first().id
    candidat.save()
    return redirect('liste_candidats', id_recrutement)

# Vue pour accepter un candidat
def accepter_candidat(request, candidat_id):
    candidat = get_object_or_404(Candidat, id=candidat_id)
    candidat.Etat_condidature = "Accepté"
    id_recrutement = candidat.Rcrt_cond.first().id
    candidat.save()
    return redirect('liste_candidats', id_recrutement)

# Vue pour la page d'accueil du manager
def acceuil_man(request):
    return render(request, 'AcceuilMan.html')



# Vue pour la liste des évaluations pour l'accès manager
def liste_evaluations_Manager(request):
    evaluations = Evaluation.objects.all()
    return render(request, 'liste_Evaluation.html', {'evaluations': evaluations})


# vue pour une nouvelle evaluation
def evaluer_employe(request, employe_id):
    if request.method == 'POST':
        form = EvaluationForm(request.POST)
        if form.is_valid():
            evaluation = form.save(commit=False)
            evaluation.Employe_Evaluation = Employe.objects.get(id=employe_id)
            evaluation.save()
            return redirect('liste_employes_Evaluations')  # Redirection vers la liste des evaluations après ajout
    else:
        form = EvaluationForm()
        return render(request, 'ajouter_evaluation.html', {'form': form})
    
# Vue pour la liste des employés pour le manager
def liste_employes_Manager(request):
    employes = Employe.objects.all()
    return render(request, 'liste_employes_Evaluations.html', {'employes': employes})

# Vue pour la page d'accueil de l'employé
def acceuil_emp(request, utilisateur_id):
    return render(request, 'AcceuilEmp.html', {'utilisateur': utilisateur_id})

# Vue pour afficher les congés d'un employé
def Mes_conges(request, utilisateur_id):
    employe = get_object_or_404(Employe, Employe_Utilisateur=utilisateur_id)
    conges = Conge.objects.filter(Employe_Conge=employe)
    return render(request, 'Mes_conges.html', {'conges': conges, 'utilisateur': utilisateur_id})
    
# Vue pour afficher les salaires d'un employé
def Mes_salaires(request, utilisateur_id):
    employee= get_object_or_404(Employe, Employe_Utilisateur=utilisateur_id)
    employee_id= employee.id
    employe = get_object_or_404(Employe, id=employee_id)
    salaires = Salaire.objects.filter(Employe_salaire=employe)
    return render(request, 'Mes_salaires.html', {'salaires': salaires, 'utilisateur': utilisateur_id})

# Vue pour afficher les contrats d'un employé
def Mes_contrats(request, utilisateur_id):
    employe = get_object_or_404(Employe, Employe_Utilisateur=utilisateur_id)
    contrats = Contrat.objects.filter(Employe_Contrat=employe)
    return render(request, 'Mes_contrats.html', {'contrats': contrats, 'utilisateur': utilisateur_id})

# Vue pour demander un congé pour un employé
def Demande_conge(request, utilisateur_id):
    if request.method == 'POST':
        form = DemandeCongeForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.employe = Employe.objects.get(Employe_Utilisateur=utilisateur_id)
            demande.statut = "En attente"
            demande.save()
            return redirect('Mes_conges', utilisateur_id)  # Redirection vers la liste des congés après ajout
    else:
        form = DemandeCongeForm()
        return render(request, 'Demande_conge.html', {'form': form, 'utilisateur': utilisateur_id})
    

# Vue pour afficher les demandes de congé d'un employé
def Mes_Demandes_conges(request, utilisateur_id):
    employe = get_object_or_404(Employe, Employe_Utilisateur=utilisateur_id)
    demandes = DemandeConge.objects.filter(employe=employe)
    return render(request, 'Mes_Demandes_conges.html', {'demandes': demandes, 'utilisateur': utilisateur_id})


# Vue pour demander une avance de salaire
def Demande_avance_salaire(request, utilisateur_id):
    if request.method == 'POST':
        form = DemandeAvanceSalaireForm(request.POST)
        if form.is_valid():
            demande = form.save(commit=False)
            demande.Employe_demande = Employe.objects.get(Employe_Utilisateur=utilisateur_id)
            demande.statut = "En attente"

           # Récupérer l'année de la date de la demande
            demandeS = DemandeAvanceSalaire.objects.filter(Employe_demande=demande.Employe_demande).order_by('-Date_demande').last()
            if demandeS :
                    if demandeS.Date_demande.year == demande.Date_demande.year :
                        demande.num_demande = demandeS.num_demande + 1
                        if demande.num_demande > 2: # Vérifier si l'employé a déjà fait 2 demandes d'avance de salaire pour la même année
                            messages = "Vous avez atteint le nombre maximum de demandes d'avance de salaire pour cette année."
                            return render(request, 'Mes_salaires.html', { 'utilisateur': utilisateur_id, 'messages': messages})
                        else:
                            demande.save()
                    else: 
                        demande.num_demande = 1
                        demande.save()
            else:
                    # Si l'employé n'a pas encore fait de demande d'avance de salaire pour l'année en cours
                   demande.num_demande = 1
                   demande.save()
            
            return redirect('Mes_salaires', utilisateur_id)  # Redirection vers la liste des salaires après ajout
    else:
        form = DemandeAvanceSalaireForm() # Créer un formulaire vide si c'est une requête GET
        return render(request, 'Demande_avance_salaire.html', {'form': form, 'utilisateur': utilisateur_id})

#Vue pour la suppression d'une demande de conge 
def Supprimer_Demande_conge(request, utilisateur_id, demande_id):
     if request.method == "POST":
        demande = get_object_or_404(DemandeConge, id=demande_id)
        demande.delete()  # Supprimer la demande
        return redirect('Mes_Demandes_conges', utilisateur_id)  # Rediriger vers la liste des demandes de conges 
     return redirect('Mes_Demandes_conges', utilisateur_id)  # Si la requête n'est pas POST, rediriger vers la liste des conges 


# vue pour la page d'acceuil du candidat 
def acceuil_candidat(request, utilisateur_id):
    return render(request, 'AcceuilCond.html', {'utilisateur': utilisateur_id})

# Vue pour afficher les recrutements pour un candidat
def liste_recrutements_Candidat(request, utilisateur_id):
    recrutements = Recrutement.objects.all()
    return render(request, 'demande_Emploi.html', {'recrutements': recrutements, 'utilisateur': utilisateur_id})


# Vue pour postuler à un recrutement
def Demande_Emploi(request, recrutement_id, utilisateur_id):
    recrutement = get_object_or_404(Recrutement, id=recrutement_id)
    candidat = Candidat.objects.get(Utilisateur_Condidat=utilisateur_id)
    recrutement.Condidat_Recrutement.add(candidat)
    messages = "Votre candidature a été envoyée avec succès."
    recrutements = Recrutement.objects.all()
    return render(request, 'demande_Emploi.html', {'utilisateur': utilisateur_id, 'recrutements' : recrutements , 'messages': messages})

from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile

def profil_employe(request, utilisateur_id):
    # Récupérer l'utilisateur et l'employé via l'ID de l'utilisateur
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    try:
        employe = utilisateur.employe  # Employé lié à l'utilisateur
    except Employe.DoesNotExist:
        return redirect('error_page')  # Si l'utilisateur n'a pas d'employé, redirige vers une page d'erreur

    # Si l'utilisateur soumet un formulaire pour modifier son profil
    if request.method == 'POST':
        form = EmployeProfileForm(request.POST, request.FILES, instance=employe)
        if form.is_valid():
            # Vérifier si une image de profil est uploadée
            if 'photo_profil' in request.FILES:
                uploaded_image = request.FILES['photo_profil']

                # Améliorer la qualité de l'image
                image = Image.open(uploaded_image)
                image = image.convert('RGB')  # Assurer que l'image est en mode RGB
                image = image.resize((300, 300))  # Redimensionner à 300x300 (ou une taille souhaitée)

                # Sauvegarder l'image traitée dans un objet fichier
                buffer = BytesIO()
                image.save(buffer, format='JPEG', quality=90)  # Qualité de 90 pour une bonne compression
                buffer.seek(0)
                processed_image = ContentFile(buffer.read(), name=uploaded_image.name)

                # Mettre à jour l'image de profil de l'employé avec l'image traitée
                employe.photo_profil = processed_image

            form.save()  # Sauvegarder les autres modifications
            return redirect('acceuil-emp', utilisateur_id=utilisateur.id)  # Rediriger vers la même page
    else:
        # Sinon, afficher le formulaire avec les données actuelles
        form = EmployeProfileForm(instance=employe)

    # Affiche le template avec le formulaire et l'employé
    return render(request, 'profil_employe.html', {'form': form, 'employe': employe, 'utilisateur': utilisateur})


def profil_candidat(request, utilisateur_id):
    utilisateur = get_object_or_404(Utilisateur, id=utilisateur_id)
    try:
        candidat = Candidat.objects.get(Utilisateur_Condidat=utilisateur)  # Correction ici
    except Candidat.DoesNotExist:
        return redirect('error_page')

    if request.method == 'POST':
        form = CandidatProfileForm(request.POST, instance=candidat)
        if form.is_valid():
            form.save()
            return redirect('acceuil-cand', utilisateur_id=utilisateur.id)
    else:
        form = CandidatProfileForm(instance=candidat)

    return render(request, 'profil_candidat.html', {
        'form': form,
        'candidat': candidat,
        'utilisateur': utilisateur,
    })


# Vue pour afficher la fiche candidature  pour un candidat
def Etat_candidature(request, utilisateur_id):
    candidat = Candidat.objects.get(Utilisateur_Condidat=utilisateur_id)
    return render(request, 'details_candidat.html', {'candidat': candidat, 'utilisateur': utilisateur_id})

#retrieve data from Employe model and convert it into a Pandas DataFrame.
def get_employe_data():
    employes = Employe.objects.all().values(
        'id', 'nom', 'prenom', 'sexe', 'date_de_naissance', 'date_aumbauche', 'Service_Employe'
    )
    df = pd.DataFrame(employes)
    return df

# Calcul de l'âge et de l'ancienneté
def calculate_age_and_seniority(df):
    today = datetime.today()
    
    # Assurez-vous que les colonnes 'date_de_naissance' et 'date_aumbauche' sont des dates
    df['date_de_naissance'] = pd.to_datetime(df['date_de_naissance'], errors='coerce')
    df['date_aumbauche'] = pd.to_datetime(df['date_aumbauche'], errors='coerce')
    
    # Calcul de l'âge
    df['age'] = df['date_de_naissance'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))
    
    # Calcul de l'ancienneté
    df['anciennete'] = df['date_aumbauche'].apply(lambda x: today.year - x.year - ((today.month, today.day) < (x.month, x.day)))
    
    return df

# Fonction pour analyser la répartition par sexe
def analyze_gender_distribution():
    df = get_employe_data()
    df = calculate_age_and_seniority(df)
    gender_count = df['sexe'].value_counts()
    return gender_count

# Fonction pour analyser la répartition par âge
def analyze_age_distribution():
    df = get_employe_data()
    df = calculate_age_and_seniority(df)
    age_bins = [20, 30, 40, 50, 60, 70, 80]
    df['age_group'] = pd.cut(df['age'], bins=age_bins, labels=['20-29', '30-39', '40-49', '50-59', '60-69', '70-79'])
    age_distribution = df['age_group'].value_counts().sort_index()
    return age_distribution

# Fonction pour analyser la répartition par ancienneté
def analyze_seniority_distribution():
    df = get_employe_data()
    df = calculate_age_and_seniority(df)
    seniority_bins = [0, 2, 5, 10, 15, 20, 30]
    df['seniority_group'] = pd.cut(df['anciennete'], bins=seniority_bins, labels=['0-2', '3-5', '6-10', '11-15', '16-20', '20+'])
    seniority_distribution = df['seniority_group'].value_counts().sort_index()
    return seniority_distribution

# Fonction pour créer un graphique de la répartition par sexe
def plot_gender_distribution():
    gender_count = analyze_gender_distribution()
    fig = px.bar(
        x=gender_count.index, 
        y=gender_count.values, 
        labels={'x': 'Gender', 'y': 'Count'},
        title="Gender Distribution of Employees"
    )
    return plot(fig, output_type="div")

# Fonction pour créer un graphique de la répartition par âge
def plot_age_distribution():
    age_distribution = analyze_age_distribution()
    fig = px.bar(
        x=age_distribution.index, 
        y=age_distribution.values, 
        labels={'x': 'Age Group', 'y': 'Count'},
        title="Age Distribution of Employees"
    )
    return plot(fig, output_type="div")

# Fonction pour créer un graphique de la répartition par ancienneté
def plot_seniority_distribution():
    seniority_distribution = analyze_seniority_distribution()
    fig = px.bar(
        x=seniority_distribution.index, 
        y=seniority_distribution.values, 
        labels={'x': 'Seniority Group', 'y': 'Count'},
        title="Seniority Distribution of Employees"
    )
    return plot(fig, output_type="div")

# Vue pour la page d'accueil ARH
def acceuil_arh(request):
    # Création des graphiques
    gender_chart = plot_gender_distribution()
    age_chart = plot_age_distribution()
    seniority_chart = plot_seniority_distribution()

    # Rendu du template avec les graphiques
    return render(request, 'AcceuilARH.html', {
        'gender_chart': gender_chart,
        'age_chart': age_chart,
        'seniority_chart': seniority_chart,
    })