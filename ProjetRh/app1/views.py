from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import loginForm, SignupForm  
from .models import Utilisateur, Candidat, Employe, Service, Competances, Formations, Recrutement, Salaire, Evaluation


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
                  return render(request, 'AgentRH.html')
                else:
                     if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'manager': # Si le login et le mot de passe sont corrects et le rôle est "manager"
                       return render(request, 'Manager.html')
                     else:
                         if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'employee': # Si le login et le mot de passe sont corrects et le rôle est "employee"
                            return render(request, 'Employe.html')
                         else:
                              if Login == utilisateur.Login and Mot_de_passe == utilisateur.mot_de_passe and utilisateur.role == 'candidate': # Si le login et le mot de passe sont corrects et le rôle est "candidate"
                                 return render(request, 'Candidat.html')
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
    
        
    