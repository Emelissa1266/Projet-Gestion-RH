from django.db import models
from django.utils import timezone

# Create your models here.
class Service(models.Model):
    Nom= models.CharField(max_length=20)
    description= models.CharField(max_length=200)


class Employe(models.Model):
    nom= models.CharField(max_length=20)
    prenom= models.CharField(max_length=20)
    date_de_naissance= models.DateField(default=timezone.now)
    date_aumbauche= models.DateField(default=timezone.now)
    adresse= models.CharField(max_length=30)
    Historique_professionnel= models.CharField(max_length=500)
    Service_Employe= models.ForeignKey(Service, on_delete=models.CASCADE)

    

class Salaire(models.Model):
    mois= models.DateField(default=timezone.now)
    annee= models.DateField(default=timezone.now)
    salaire_base= models.FloatField(max_length=15)
    primes=models.FloatField(max_length=15)
    heures_supplementaires= models.IntegerField(max_length=5)
    retenus= models.FloatField(max_length=15)
    salaire_net= models.FloatField(max_length=20)
    Employe_salaire= models.ForeignKey(Employe, on_delete=models.CASCADE)


class Evaluation(models.Model):
    date_Evaluation= models.DateField(default=timezone.now)
    criteres= models.CharField(max_length=200)
    Resultat= models.CharField(max_length=200)
    Commentaire= models.CharField(max_length=500)
    Employe_Evaluation= models.ForeignKey(Employe, on_delete=models.CASCADE)




class Conge(models.Model):
    date_deb= models.DateField(default=timezone.now)
    date_fin= models.DateField(default=timezone.now)
    type_conge= models.CharField(max_length=15)
    solde_conge= models.FloatField(max_length= 10)
    Employe_Conge= models.ForeignKey(Employe, on_delete=models.CASCADE)



class Contrat(models.Model):
     date_deb= models.DateField(default=timezone.now)
     date_fin= models.DateField(default=timezone.now)
     type_contrat= models.CharField(max_length=15)
     salaire_monsuel= models.FloatField(max_length=20)
     salaire_quotidien= models.FloatField(max_length=20)
     Employe_Contrat= models.ForeignKey(Employe, on_delete=models.CASCADE)

