from django.contrib import admin
from django.urls import path 
from . import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.RedirectionVersPage, name='connexion'),
    path('home/signup/', views.signup, name='inscription'),  # Ajoute une vue pour l'inscription
    path('home/', views.home_candidat, name='homecandidat'),  # Page d'accueil 
    path('acceuil-arh/', views.acceuil_arh, name='acceuil_arh'),
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
    path('acceuil-arh/contrats/supprimer/<int:contrat_id>/', views.supprimer_contrat, name='supprimer_contrat'),
    path('acceuil-arh/contrats/liste_archive/', views.liste_archives_contrats, name='liste_archive_contrat'),
    path('acceuil-arh/recrutements/', views.liste_recrutements, name='liste_recrutements'),
    path('acceuil-arh/recrutements/modifier/<int:recrutement_id>/', views.modifier_recrutement, name='modifier_recrutement'),
    path('acceuil-arh/recrutements/details_recrutement/<int:recrutement_id>/', views.details_recrutement, name='details_recrutement'),
    path('acceuil-arh/recrutements/supprimer_recrutement/<int:recrutement_id>/', views.supprimer_recrutement, name='supprimer_recrutement'),
    path('acceuil-arh/recrutements/ajouter_recrutement/', views.ajouter_recrutement, name='ajouter_recrutement'),
    path('acceuil-arh/recrutements/liste_candidats/<int:recrutement_id>/', views.liste_candidats, name='liste_candidats'),
    path('acceuil-arh/recrutements/details_candidat/<int:candidat_id>/', views.details_candidat, name='details_candidat'),
    path('acceuil-arh/recrutements/refuser_candidat/<int:candidat_id>/', views.refuser_candidat, name='refuser_candidat'),
    path('acceuil-arh/recrutements/accepter_candidat/<int:candidat_id>/', views.accepter_candidat, name='accepter_candidat'),
    path('acceuil-man/', views.acceuil_man, name='acceuil-man'),
    path('acceuil-man/evaluer_employe/<int:employe_id>/', views.evaluer_employe, name='evaluer_employe'),
    path('acceuil-man/evaluations/', views.liste_evaluations_Manager, name='liste_employes_Evaluations'),
    path('acceuil-man/liste_employee/', views.liste_employes_Manager, name='liste_Employes'),
    path('acceuil-emp/<int:utilisateur_id>/', views.acceuil_emp, name='acceuil-emp'),
    path('acceuil-emp/Mes_conges/<int:utilisateur_id>/', views.Mes_conges, name='Mes_conges'),
    path('acceuil-emp/Mes_salaires/<int:utilisateur_id>/', views.Mes_salaires, name='Mes_salaires'),
    path('acceuil-emp/Mes_contrats/<int:utilisateur_id>/', views.Mes_contrats, name='Mes_contrats'),
    path('acceuil-emp/profil/<int:utilisateur_id>/', views.profil_employe, name='profil_employe'),
    path('acceuil-emp/Demande_conge/<int:utilisateur_id>/', views.Demande_conge, name='Demande_conge'),
    path('acceuil-emp/Mes_Demandes_conges/<int:utilisateur_id>', views.Mes_Demandes_conges, name='Mes_Demandes_conges'),
    path('acceuil-emp/Mes_Demandes_conges/supprimer_demande_conge/<int:utilisateur_id>/<int:demande_id>/', views.Supprimer_Demande_conge, name='Supprimer_Demande_conge'),
    path('acceuil-emp/Demande_avance_salaire/<int:utilisateur_id>/', views.Demande_avance_salaire, name='Demande_avance_salaire'),
    path('acceuil-cand/MonProfil/<int:utilisateur_id>/', views.profil_candidat, name='profil_candidat'),
    path('acceuil-cand/<int:utilisateur_id>/', views.acceuil_candidat, name='acceuil-cand'),
    path('acceuil-cand/Demande_Emploi/<int:utilisateur_id>/', views.liste_recrutements_Candidat, name='demande_emploi'),
    path('acceuil-cand/Demande_Emploi/<int:utilisateur_id>/<int:recrutement_id>', views.Demande_Emploi, name='demande_emploi'),
    path('acceuil-cand/Etat_candidature/<int:utilisateur_id>/', views.Etat_candidature, name='etat_candidature'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

