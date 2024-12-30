from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.hashers import make_password, check_password
from .forms import loginForm, SignupForm  ,EmployeForm ,UtilisateurForm ,CongeForm
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation ,Conge ,DemandeConge
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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
                            return render(request, 'AcceuilEmp.html')
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

# Vue pour la liste des congés
def liste_conges(request):
    conges = Conge.objects.all()
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

def liste_demandes_conges(request):
    demandes_conges = DemandeConge.objects.all()
    return render(request, 'liste_demande.html', {'demandes_conges': demandes_conges})
