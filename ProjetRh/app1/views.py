from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from .forms import loginForm, SignupForm  
from .models import Utilisateur, Candidat


def home_candidat(request):
    return render(request, 'home_candidat.html')


def authentifier(request):
    if request.method == "POST":
        form = loginForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            mot_de_passe = form.cleaned_data["mot_de_passe"]
            try:
                utilisateur = Utilisateur.objects.get(Login=login)
                if check_password(mot_de_passe, utilisateur.mot_de_passe):
                    # Stocker l'utilisateur dans la session
                    request.session["utilisateur_id"] = utilisateur.id
                    return redirect("services")  # Redirection après connexion réussie
                else:
                    form.add_error('login', "Login ou mot de passe incorrect !")
            except Utilisateur.DoesNotExist:
                form.add_error('login', "Login ou mot de passe incorrect !")
    else:
        form = loginForm()
    return render(request, "login.html", {"form": form})


# Vue pour l'inscription
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # Sauvegarder l'utilisateur sans le valider pour ajouter le rôle
            utilisateur = form.save(commit=False)
            utilisateur.mot_de_passe = make_password(utilisateur.mot_de_passe)  # Hacher le mot de passe
            utilisateur.role = 'candidate'  # Par défaut, le rôle est "candidate"
            utilisateur.save()  # Sauvegarder l'utilisateur

            # Créer un candidat associé à l'utilisateur
            Candidat.objects.create(
                Nom=utilisateur.nom,
                Prenom=utilisateur.prenom,
                Utilisateur_Condidat=utilisateur,
                Email=form.cleaned_data['email'],  # Utiliser l'email fourni par l'utilisateur
                Etat_condidature="en attente"  # Etat par défaut pour un candidat
            )

            return redirect('connexion')  # Redirige vers la page de connexion après l'inscription
    else:
        form = SignupForm()  # Créer un formulaire vide si c'est une requête GET

    return render(request, 'signup.html', {'form': form})