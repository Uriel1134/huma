from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import FormView
from .forms import SignupForm
from django.contrib.auth import login, authenticate, logout
# from django.contrib.auth.views import LoginView, LogoutView


from recruit.models import Ecole, Enseignant, Evaluateur

def signup(request):
    if request.method == 'POST':
        register_form = SignupForm(request.POST)
        if register_form.is_valid():
            # Enregistrement de l'utilisateur
            user = register_form.save(commit=False)
            user.save()  # Sauvegarde de l'utilisateur
            
            # Récupération du choix du groupe
            group_choice = register_form.cleaned_data['groups']
            
            # Création de l'instance appropriée dans la bonne table
            if group_choice == 5:  # ID pour "Ecole"
                Ecole.objects.create(
                    created_by=user,
                    nom="Nom de l'école",  # Remplacez par des valeurs réelles ou des champs du formulaire
                    email="email@ecole.com",  # Valeurs par défaut ou à récupérer
                    adresse="Adresse de l'école",
                    description="Description de l'école",
                    contact="12345678"
                )
            elif group_choice == 6:  # ID pour "Enseignant"
                Enseignant.objects.create(
                    created_by=user,
                    nom="Nom de l'enseignant",
                    prenom="Prénom de l'enseignant",
                    adresse="Adresse de l'enseignant",
                    contact="87654321",
                    email="email@enseignant.com",
                    diplome=None,  # Remplacez par une valeur réelle
                    grade=None,    # Remplacez par une valeur réelle
                    spec=None      # Remplacez par une valeur réelle
                )
            elif group_choice == 7:  # ID pour "Evaluateur"
                Evaluateur.objects.create(
                    created_by=user,
                    nom="Nom de l'évaluateur",
                    prenom="Prénom de l'évaluateur",
                    email="email@evaluateur.com",
                    contact="11223344",
                    diplome=None,  # Remplacez par une valeur réelle
                    grade=None,    # Remplacez par une valeur réelle
                    spec=None      # Remplacez par une valeur réelle
                )
            
            # Connexion automatique de l'utilisateur
            login(request, user)
            
            # Redirection après inscription
            return redirect('recruit:profil_creation')
    else:
        register_form = SignupForm()

    context = {'signup': register_form}
    return render(request, 'register.html', context=context)

def logouts(request: HttpRequest):
    logout(request)
    return redirect('recruit:home')

