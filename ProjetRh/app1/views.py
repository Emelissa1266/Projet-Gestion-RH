from django.shortcuts import render, redirect
from .forms import AuthentificationForm
from .models import Utilisateur

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
    return render(request, "authentification.html", {"form": form})
