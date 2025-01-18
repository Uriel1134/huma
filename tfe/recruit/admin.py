from django.contrib import admin
from .models import *

@admin.register(Ecole)
class EcoleAdmin(admin.ModelAdmin):
  list_display = ('nom', 'email', 'adresse', )

@admin.register(Appel)
class AppelAdmin(admin.ModelAdmin):
  list_display = ('titre', 'description', 'date_fin')

@admin.register(Parametre)
class ParametreAdmin(admin.ModelAdmin):
  list_display = ('type', 'titre', )

@admin.register(Specialite)
class SpecialiteAdmin(admin.ModelAdmin):
  list_display = ('intitule', 'description', )

@admin.register(Enseignant)
class EnseignantAdmin(admin.ModelAdmin):
  list_display = ('nom', 'prenom', 'adresse', )

@admin.register(Candidature)
class CandidatureAdmin(admin.ModelAdmin):
  list_display = ('enseignant', 'appel', 'date_soumission')

@admin.register(Evaluateur)
class EvaluateurAdmin(admin.ModelAdmin):
  list_display = ('nom', 'prenom',)


@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
  list_display = ('acronyme', )
  search_fields = ('acronyme',)

@admin.register(UE)
class UEAdmin(admin.ModelAdmin):
  list_display = ('nom', 'sys_name', )
  search_fields = ('nom', )

@admin.register(Evaluation)
class EvaluationAdmin(admin.ModelAdmin):
  list_display = ('candidature', 'evaluateur', 'departement', 'decision')
  search_fields = ('decision', )
  list_filter = ('pieces', 'decision')
