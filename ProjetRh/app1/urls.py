from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.RedirectionVersPage, name='connexion'),
    path('home/signup/', views.signup, name='inscription'),  # Ajoute une vue pour l'inscription
    path('home/', views.home_candidat, name='homecandidat'),  # Page d'accueil 
    path('acceuil-arh/', views.acceuil_arh, name='acceuil_arh'),  # URL pour la page d'accueil ARH
    path('employes/', views.liste_employes, name='liste_employes'),
    path('employes/ajouter/', views.ajouter_employe, name='ajouter_employe'),
    path('employes/modifier/<int:employe_id>/', views.modifier_employe, name='modifier_employe'),
    path('employes/supprimer/<int:employe_id>/', views.supprimer_employe, name='supprimer_employe'),
    path('employes/detail/<int:employe_id>/', views.detail_employe, name='Fiche_employe'),
    path('employes/evaluation/', views.liste_evaluations, name='liste_evaluations'),
    path('employes/evaluation/rapport/<int:evaluation_id>/', views.rapport_evaluation, name='rapport_evaluation'),
    path('employes/evaluation/suppimer_evaluation/<int:evaluation_id>/', views.supprimer_evaluation, name='supprimer_evaluation'),
    path('acceuil-arh/conges/',views.liste_conges, name='liste_conges'),
    path('acceuil-arh/conges/ajouter/', views.ajouter_conge, name='ajouter_conge'),
    path('acceuil-arh/conges/Liste_dmconge/', views.liste_demandes_conges, name='liste_demande_conge'),
    path('acceuil-arh/conges/supprimer_conge/<int:conge_id>/', views.supprimer_conge, name='supprimer_conge'),
    path('accepter_demande/<int:demande_id>/', views.accepter_demande_conge, name='accepter_demande'),
    path('refuser_demande/<int:demande_id>/', views.refuser_demande_conge, name='refuser_demande'),
    path('acceuil-arh/salaires/', views.liste_salaires, name='liste_salaires'),
    path('acceuil-arh/salaires/ajouter_salaire/', views.ajouter_salaire, name='ajouter_salaire'),
    path('acceuil-arh/salaires/supprimer_salaire/<int:salaire_id>/', views.supprimer_salaire, name='supprimer_salaire'),
    path('acceuil-arh/salaires/Fiche_paie/<int:salaire_id>/', views.fiche_paie, name='fiche_paie'),
    path('acceuil-arh/salaires/demande_avance_salaire/', views.liste_demande_avance_salaire, name='avance_salaire'),
    path('acceuil-arh/salaires/demande_avance_salaire/accepter/<int:demande_id>/', views.accepter_demande_avance_salaire, name='accepter_demande_avance_salaire'),
    path('acceuil-arh/salaires/demande_avance_salaire/refuser/<int:demande_id>/', views.refuser_demande_avance_salaire, name='refuser_demande_avance_salaire'),
    path('acceuil-arh/contrats/', views.liste_contrats, name='liste_contrats'),
    path('acceuil-arh/contrats/ajouter/', views.ajouter_contrat, name='ajouter_contrat'),
    path('acceuil-arh/contrats/modifier/<int:contrat_id>/', views.modifier_contrat, name='modifier_contrat'),
    path('acceuil-arh/contrats/consulter/<int:contrat_id>/', views.consulter_contrat, name='consulter_contrat'),
]

