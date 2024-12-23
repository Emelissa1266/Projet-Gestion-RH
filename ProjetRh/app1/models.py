from django.db import models
from django.utils import timezone

# Create your models here.
class Service(models.Model):
    Nom= models.CharField(max_length=20)
    description= models.CharField(max_length=200)


class Utilisateur(models.Model):
    Login = models.CharField(max_length= 30, unique=True)
    mot_de_passe = models.CharField(max_length=20)
    role = models.CharField(max_length=30)


class Competances(models.Model):
    descripton= models.CharField(max_length=40)

class Formations(models.Model):
    nom_formation= models.CharField(max_length=20)
    date_obtention= models.DateField(default=timezone.now)
   


class Employe(models.Model):
    nom= models.CharField(max_length=20)
    prenom= models.CharField(max_length=20)
    date_de_naissance= models.DateField(default=timezone.now)
    date_aumbauche= models.DateField(default=timezone.now)
    adresse= models.CharField(max_length=30)
    Historique_professionnel= models.CharField(max_length=500)
    Service_Employe= models.ForeignKey(Service, on_delete=models.CASCADE)
    Competance_Employe=models.ManyToManyField(Competances, related_name="comp")
    Employe_Formation= models.ManyToManyField(Formations, related_name="frm")
    

    

class Salaire(models.Model):
    mois= models.DateField(default=timezone.now)
    annee= models.DateField(default=timezone.now)
    salaire_base= models.FloatField(max_length=15)
    primes=models.FloatField(max_length=15)
    heures_supplementaires= models.IntegerField(default=0)
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





class Condidat (models.Model):
    Nom= models.CharField(max_length= 20)
    Prenom= models.CharField(max_length= 20)
    Email= models.CharField(max_length= 30)
    CV = models.CharField(max_length= 500)
    date_condidature= models.DateField(default=timezone.now)
    Utilisateur_Condidat= models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    Etat_condidature= models.CharField(max_length=30)


class Recrutement(models.Model):
    offre_emploi= models.CharField(max_length=40)
    description= models.CharField(max_length= 500)
    status= models.CharField(max_length=100)
    Condidat_Recrutement= models.ManyToManyField(Condidat, related_name="Rcrt_cond")
   






