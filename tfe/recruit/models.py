#Définir des modèles qui représentent les tables de la base de données
from django.db import models
#Le modèle User pour gérer les users ainsi que leur authentification
from django.contrib.auth.models import User
#Définir les rèles de validation basées sur les expressions régulières
from django.core.validators import RegexValidator


class Ecole(models.Model):
  #L'utilisateur qui a créé l'école qui est associer à un seul utilisateur
  #OneToOneField: Relation 1-1 avec un utilisateur.
  #on_delete=models.CASCADE: Supprime l'école si l'utilisateur est supprimé.
  created_by = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE) 
  nom = models.CharField(max_length=100, unique=True, blank=False, null=False)
  email = models.EmailField(max_length=254, blank=False, null=False, unique=True)
  adresse = models.CharField(max_length=255, blank=False, null=False)
  photo = models.ImageField(upload_to='ecoles/photos/', blank=False, null=True)
  description = models.TextField(blank=False, null=False, default='')
  contact = models.CharField(max_length=8, validators=[RegexValidator(regex=r'^\d+$', message='Uniquement des chiffres'),], blank=False, null=False)
  
  def __str__(self):
    return self.nom  
  class Meta:
    verbose_name = "Ecole"
    verbose_name_plural = "Ecoles"  



class Appel(models.Model):
  #Chaque appel est lié à une école. (Relation ForeignKey= plusieurs appels par école).
  ecole = models.ForeignKey(Ecole, on_delete=models.CASCADE, blank=False)
  titre = models.CharField(max_length=50, blank=False, null=False)
  description = models.TextField(max_length=500, blank=False, null=False, default='')
  nbr_poste = models.PositiveIntegerField(default=0) 
  mission = models.CharField(max_length=255, blank=False, null=False)
  date_debut = models.DateField(auto_now=False, auto_now_add=True)
  date_fin = models.DateField(auto_now=False, auto_now_add=False, blank=False, null=False)
  document = models.FileField(upload_to='documents/', blank=True, null=True) 
  
  def __str__(self):
    return self.titre
  
  class Meta:
    verbose_name = "Appel"
    verbose_name_plural = "Appels"     


class Parametre(models.Model):
  choix = [("dip", "Diplôme"), ("gde", "Grade")]
  type = models.CharField(max_length=50, choices=choix, default="dip", blank=False, null=False)
  titre = models.CharField(max_length=255, blank=False, null=False)
  description = models.TextField(default='')
  
  def __str__(self):
    return self.titre
  class Meta:
    verbose_name = "Paramètre"
    verbose_name_plural = "Paramètres"  


class Specialite(models.Model):
  intitule = models.CharField(max_length=150, verbose_name='intitulé', unique=True, blank=False, null=False)
  description = models.TextField(max_length=500, default='')
  sys_name = models.CharField(max_length=20)
  
  def __str__(self):
    return self.intitule  
  class Meta:
    verbose_name = "Spécialité"
    verbose_name_plural = "Spécialités"  


class Enseignant(models.Model):
  created_by = models.OneToOneField(User, primary_key=True ,on_delete=models.CASCADE)
  nom = models.CharField(max_length=255, blank=False, null=False)
  prenom = models.CharField(max_length=255, blank=False, null=False)
  adresse = models.CharField(max_length=255, blank=False, null=False)
  contact = models.CharField(max_length=8, validators=[RegexValidator(regex=r'^\d+$', message='Uniquement des chiffres'),], blank=False, null=False)
  email = models.EmailField(blank=False, null=False, unique=True)
  photo = models.ImageField(upload_to='enseignants/photos/', blank=False, null=True)
  diplome = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='enseignant_diplome', limit_choices_to={"type": "dip"}, blank=False)
  grade = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='enseignant_grade', limit_choices_to={"type": "gde"}, blank=False)
  spec = models.ForeignKey(Specialite, on_delete=models.CASCADE, blank=False)
  
  def __str__(self):
    return f'{self.prenom} {self.nom}' 
  class Meta:
    verbose_name = "Enseignant"
    verbose_name_plural = "Enseignants" 
    unique_together = ["nom", "prenom"]

from django.core.exceptions import ValidationError
def file_validator(file):
  if not(file.name.endswith(".pdf")):
    raise ValidationError("Seul les pdf sont autorisés")

class Candidature(models.Model):
  appel = models.ForeignKey(Appel, verbose_name="école", on_delete=models.CASCADE, blank=False)
  enseignant = models.ForeignKey(Enseignant, on_delete=models.CASCADE, blank=False)
  cv = models.FileField(verbose_name="CV", upload_to="enseignants/fichiers/", max_length=100, blank=False)
  demande = models.ImageField(upload_to='enseignants/photos/', blank=True, null=True, verbose_name="Demande manuscrite")  
  diplome = models.FileField(verbose_name="diplome",  upload_to="enseignants/fichiers/", max_length=100, blank=True, null=True)
  ifu = models.FileField(verbose_name="IFU", upload_to="enseignants/fichiers/", max_length=100, blank=True, null=True, validators=[file_validator])
  rib = models.FileField(verbose_name="RIB", upload_to="enseignants/fichiers/", max_length=100, blank=True, null=True, validators=[file_validator])
  date_soumission = models.DateField(auto_now=False, auto_now_add=True, blank=False)
  autre = models.FileField(upload_to="enseignants/fichiers/", max_length=100, verbose_name="Attestations formations", blank=True, null=True, validators=[file_validator])
  statut = models.CharField(max_length=100, choices=[('attente', 'En cours'), ('fini', 'Terminé')], default='attente', blank=False)
  
  def __str__(self):
    return f'{self.enseignant}'   
  class Meta:
    verbose_name = "Candidature"
    verbose_name_plural = "Candidatures"   


class Evaluateur(models.Model):
  created_by = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, blank=False)
  nom = models.CharField(max_length=255, blank=False, null=False)
  prenom = models.CharField(max_length=255, blank=False, null=False)
  email = models.EmailField( blank=False, null=False, unique=True)
  contact = models.CharField(max_length=8, validators=[RegexValidator(regex=r'^\d+$', message='Uniquement des chiffres'),], blank=False, null=False)
  diplome = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='evaluateur_diplome', limit_choices_to={"type": "dip"}, blank=False)
  grade = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='evaluateur_grade', limit_choices_to={"type": "gde"}, blank=False)
  spec = models.ForeignKey(Specialite, verbose_name="spécialité", on_delete=models.CASCADE, blank=False)
  
  def __str__(self):
    return self.nom
  class Meta:
    verbose_name = "Evaluateur"
    verbose_name_plural = "Evaluateurs" 
    unique_together = ["nom", "prenom"]


class Departement(models.Model):
  acronyme = models.CharField(max_length=15, blank=False, null=False)
  description = models.TextField(default='', blank=False)
  
  def __str__(self):
    return self.acronyme  
  class Meta:
    verbose_name = "Département"
    verbose_name_plural = "Départements" 


class UE(models.Model):
  nom = models.CharField(max_length=60, blank=False)
  depart = models.ForeignKey(Departement, verbose_name="Département", on_delete=models.CASCADE, null=True, blank=False)
  sys_name = models.CharField(max_length=20, blank=False)
  description = models.TextField(default='', blank=False)
  
  def __str__(self):
    return self.nom  


class Evaluation(models.Model):
  haut_diplome = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='evaluation_diplome', limit_choices_to={"type": "dip"}, null=True, blank=False)
  grade = models.ForeignKey(Parametre,  on_delete=models.CASCADE, related_name='evaluation_grade', limit_choices_to={"type": "gde"}, null=True, blank=False)
  spec = models.ForeignKey(Specialite, on_delete=models.SET_NULL, null=True, blank=False)
  departement = models.ForeignKey(Departement, on_delete=models.SET_NULL, null=True, blank=False)
  candidature = models.ForeignKey(Candidature, on_delete=models.CASCADE, blank=False)
  evaluateur = models.ForeignKey(Evaluateur, on_delete=models.CASCADE, blank=False)
  ans_ecole = models.PositiveIntegerField(verbose_name='Ancienneté dans l\'école', default=0, blank=False)
  ue_spec = models.BooleanField(verbose_name='Adéquation UE_Spécialité', help_text='adéquation UE spécialité', default=False, blank=False)
  an_ens = models.PositiveIntegerField(verbose_name='Ancienneté', help_text='Ancienneté dans l\'enseignement', default=0, blank=False)
  formation_justifie = models.BooleanField(help_text='Formation justifié en cas d\'attestation', default=False, blank=False)
  exp_entreprise = models.PositiveIntegerField(help_text='Expérience en entreprise', default=0, blank=False)
  age = models.PositiveIntegerField(default=0, blank=False)
  pieces = models.CharField(max_length=255, choices=[('comp','Complet'), ('inc','Incomplet')], default='inc', blank=False)
  decision = models.CharField(max_length=255, verbose_name='Décision' ,choices=[('oui','Recevable'), ('revoir','Réservé'), ('non','Non recevable')], default='revoir', blank=False)
  observation = models.TextField(default='', blank=False)

  def __str__(self):
    return self.evaluateur.nom
  class Meta: 
    verbose_name = "Evaluation"
    verbose_name_plural = "Evaluations"


