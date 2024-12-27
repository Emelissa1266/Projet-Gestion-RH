from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('login/', views.RedirectionVersPage, name='connexion'),
    path('signup/', views.signup, name='inscription'),  # Ajoute une vue pour l'inscription
    path('home/', views.home_candidat, name='homecandidat'),  # Page d'accueil 
]

