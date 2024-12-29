from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.RedirectionVersPage, name='connexion'),
    path('signup/', views.signup, name='inscription'),  # Ajoute une vue pour l'inscription
    path('home/', views.home_candidat, name='homecandidat'),  # Page d'accueil 
     path('acceuil-arh/', views.acceuil_arh, name='acceuil_arh'),  # URL pour la page d'accueil ARH
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:employe_id>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:employe_id>/', views.supprimer_employe, name='supprimer_employe'),
]

