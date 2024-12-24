from django.shortcuts import render, redirect
from .forms import AuthentificationForm
from .models import Utilisateur
from .forms import SignupForm

def home_candidat(request):
    return render(request, 'home_candidat.html')

def authentifier(request):
    if request.method == "POST":
        form = AuthentificationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            mot_de_passe = form.cleaned_data["mot_de_passe"]
            try:
                utilisateur = Utilisateur.objects.get(Login=login, mot_de_passe=mot_de_passe)
                # Stocker l'utilisateur dans la session
                request.session["utilisateur_id"] = utilisateur.id
                return redirect("services")  # Redirection après connexion réussie
            except Utilisateur.DoesNotExist:
                form.add_error(None, "Login ou mot de passe incorrect !")
    else:
        form = AuthentificationForm()
        return render(request, "login.html", {"form": form})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            utilisateur = form.save(commit=False)
            utilisateur.role = 'candidate'  # Par défaut, le rôle est "candidate"
            utilisateur.save()
            return redirect('connexion')  # Redirige vers la page de connexion
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})
