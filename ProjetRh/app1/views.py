from django.shortcuts import render
from .forms import AuthentificationForm
from .models import Utilisateur
from django.shortcuts import redirect

# Create your views here.
from django.shortcuts import render
def authentifier(request):
    if request.method == "POST":
        form = AuthentificationForm(request.POST)
        if form.is_valid():
            login = form.cleaned_data["login"]
            mot_de_passe = form.cleaned_data["mot_de_passe"]
            try:
                utilisateur = Utilisateur.objects.get(login=login, mot_de_passe=mot_de_passe)
                request.session["utilisateur"] = utilisateur.id
                return redirect("services")
            except Utilisateur.DoesNotExist:
                form.add_error(None, "Login ou mot de passe incorrect! Si vous n'avez pas un compte creer un")
    else:
        form = AuthentificationForm()
    return render(request, "authentification.html", {"form": form})