from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import loginForm, SignupForm  ,EmployeForm ,UtilisateurForm ,CongeForm, SalaireForm, ContratForm, RecrutementForm, EvaluationForm, DemandeCongeForm
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation ,Conge ,DemandeConge, DemandeAvanceSalaire, Contrat, ArchiveContrat
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login


def home_candidat(request):
    return render(request, 'home_candidat.html')

# Vue pour l'inscription
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
           # Sauvegarder l'utilisateur sans le valider pour ajouter le rôle
            Utilisateur =  form.save(commit=False)
            Utilisateur.Login = form.cleaned_data['Login']
            Utilisateur.mot_de_passe = make_password(form.cleaned_data['mot_de_passe'])  # Hacher le mot de passe
            Utilisateur.role = 'candidate'  # Par défaut, le rôle est "candidate"
            
            form.save()  # Sauvegarder l'utilisateur

            # Créer un candidat associé à l'utilisateur
            Candidat.objects.create(
                 Nom=Utilisateur.nom,
                 Prenom=Utilisateur.prenom,
                 Utilisateur_Condidat=Utilisateur,
                 Email=Utilisateur.Login,  # Utiliser l'email fourni par l'utilisateur
                 Etat_condidature="en attente"  # Etat par défaut pour un candidat
             )

            return redirect('connexion')  # Redirige vers la page de connexion après l'inscription
    else:
        form = SignupForm()  # Créer un formulaire vide si c'est une requête GET

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
                  return render(request, 'AcceuilARH.html')
                else:
                     if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'manager': # Si le login et le mot de passe sont corrects et le rôle est "manager"
                       return render(request, 'AcceuilMan.html')
                     else:
                         if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'employee': # Si le login et le mot de passe sont corrects et le rôle est "employee"
                            return render(request, 'AcceuilEmp.html', {'utilisateur': utilisateur.id})
                         else:
                              if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'candidate': # Si le login et le mot de passe sont corrects et le rôle est "candidate"
                                 return render(request, 'AcceuilCond.html')
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
    


    
    
def acceuil_arh(request):
    return render(request, 'AcceuilARH.html')


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
    return render(request, 'liste_Employe.html', {'employes': employes})

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