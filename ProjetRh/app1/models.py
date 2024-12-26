from django.db import models
from django.utils import timezone

# Modèle pour les services

class Service(models.Model):
    Nom= models.CharField(max_length=20)
    description= models.CharField(max_length=200)
    def __str__(self):
        return self.nom


# Modèle pour les utilisateurs
class Utilisateur(models.Model):
    Login = models.CharField(max_length= 30, unique=True)
    mot_de_passe = models.CharField(max_length=20)
    nom = models.CharField(max_length=30, blank=True, null=True)
    prenom = models.CharField(max_length=30, blank=True, null=True)
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('candidate', 'Candidate'),
    ]
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='candidate')

    def __str__(self):
        return self.login

# Modèle pour les compétences
class Competances(models.Model):
    descripton= models.CharField(max_length=40)


    def __str__(self):
        return self.description

# Modèle pour les formations
class Formations(models.Model):
    nom_formation= models.CharField(max_length=20)
    date_obtention= models.DateField(default=timezone.now)
    description= models.CharField(max_length=200)

    def __str__(self):
        return self.nom_formation
   

# Modèle pour les employés
class Employe(models.Model):
    nom= models.CharField(max_length=20)
    prenom= models.CharField(max_length=20)
    date_de_naissance= models.DateField(default=timezone.now)
    date_aumbauche= models.DateField(default=timezone.now)
    adresse= models.CharField(max_length=30)
    Historique_professionnel= models.CharField(max_length=500)
    Service_Employe= models.ForeignKey(Service, on_delete=models.CASCADE)
    Competance_Employe=models.ManyToManyField(Competances, related_name="comp", blank=True)
    Employe_Formation= models.ManyToManyField(Formations, related_name="frm", blank=True)
    Employe_Utilisateur= models.OneToOneField(Utilisateur, on_delete=models.CASCADE, related_name="employe")

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

    
# Modèle pour les salaires
class Salaire(models.Model):
    mois_annee= models.DateField(default=timezone.now)
    salaire_base= models.FloatField(max_length=15)
    primes=models.FloatField(max_length=15)
    heures_supplementaires= models.IntegerField(default=0)
    retenus= models.FloatField(max_length=15)
    salaire_net= models.FloatField(max_length=20)
    Employe_salaire= models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="salaires")

    def __str__(self):
        return f"Salaire pour {self.employe.nom} - {self.mois}"


# Modèle pour les évaluations
class Evaluation(models.Model):
    date_Evaluation= models.DateField(default=timezone.now)
    criteres= models.CharField(max_length=200)
    Resultat= models.CharField(max_length=200)
    Commentaire= models.CharField(max_length=500)
    Employe_Evaluation= models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="evaluations")

    def __str__(self):
        return f"Évaluation de {self.employe.nom} - {self.date_evaluation}"



# Modèle pour les congés
class Conge(models.Model):
    date_deb= models.DateField(default=timezone.now)
    date_fin= models.DateField(default=timezone.now)
    TYPE_CHOICES = [
        ('paid', 'Paid Leave'),
        ('sick', 'Sick Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('maternity', 'Maternity Leave'),]
    type_conge = models.CharField(max_length=15, choices=TYPE_CHOICES)
    solde_conge= models.FloatField(max_length= 10)
    Employe_Conge= models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="conges")

    def __str__(self):
        return f"Congé de {self.employe.nom} - {self.type_conge}"


# Modèle pour les contrats
class Contrat(models.Model):
     date_deb= models.DateField(default=timezone.now)
     date_fin= models.DateField(default=timezone.now)
     TYPE_CHOICES = [
        ('permanent', 'Permanent'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
    ]
     type_contrat= models.CharField(max_length=15, choices=TYPE_CHOICES)
     salaire_monsuel= models.FloatField(max_length=20)
     salaire_quotidien= models.FloatField(max_length=20)
     Employe_Contrat= models.ForeignKey(Employe, on_delete=models.CASCADE, related_name="contrats")

     def __str__(self):
        return f"Contrat de {self.employe.nom} - {self.type_contrat}"


# Modèle pour les condidats
class Candidat (models.Model):
    Nom= models.CharField(max_length= 20)
    Prenom= models.CharField(max_length= 20)
    Email= models.CharField(max_length= 30, unique=True)
    CV = models.TextField()
    date_condidature= models.DateField(default=timezone.now)
    Utilisateur_Condidat= models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="condidats")
    Etat_condidature= models.CharField(max_length=30)

    def __str__(self):
        return f"{self.prenom} {self.nom}"
    

# Modèle pour les recrutements
class Recrutement(models.Model):
    offre_emploi= models.CharField(max_length=40)
    description= models.CharField(max_length= 500)
    status= models.CharField(max_length=100)
    date_debut= models.DateField(default=timezone.now)
    Condidat_Recrutement= models.ManyToManyField(Candidat, related_name="Rcrt_cond")

    def __str__(self):
        return self.offre_emploi
    






