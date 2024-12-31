from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('home/', views.home_candidat, name='homecandidat'),  # Page d'accueil
    path('login/', views.RedirectionVersPage, name='connexion'),
    path('home/signup/', views.signup, name='inscription'),  # Ajoute une vue pour l'inscription  # Page d'accueil 
    path('home/login/motdepasseoublie/', views.motdepasseoublie, name='password_reset'),  # Ajoute une vue pour le mot de passe oublié
     path('acceuil-arh/', views.acceuil_arh, name='acceuil_arh'),  # URL pour la page d'accueil ARH
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:employe_id>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:employe_id>/', views.supprimer_employe, name='supprimer_employe'),
    path('acceuil-arh/conges/',views.liste_conges, name='liste_conges'),
    path('acceuil-arh/conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('acceuil-arh/conges/Liste_dmconge/', views.liste_demandes_conges, name='liste_demande_conge'),
    path('confirmer-email/<str:confirmation_code>/', views.confirmer_email, name='confirmer_email'),
]

