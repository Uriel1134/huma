from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .models import *
from .forms import *
from django.views.generic import ListView
from django.utils import timezone
from django.contrib.auth import logout
from .forms import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from .models import Enseignant, Evaluateur

from django.shortcuts import render
from .models import Appel

def accueil(request):
    appels = Appel.objects.all()
    return render(request, 'accueil.html', {'appels': appels})

def appels(request):
    appels = Appel.objects.all()
    return render(request, 'appels.html', {'appels': appels})

def group_check(user):
  return user.groups.filter(name__in=['Evaluateur', 'Enseignant', 'Ecole']).exists()

# def accueil(request:HttpRequest):
#   return render(request, 'accueil.html')

@user_passes_test(group_check)
def dash(request:HttpRequest):
  appel = Appel.objects.filter(date_fin__gte=timezone.now())
  return render(request, 'dashboard.html', context={'appels':appel})

class EcoleCreateView( CreateView ):
  model = Ecole
  fields = ['nom', 'email', 'adresse', 'description', 'contact', 'photo']
  template_name = 'profil.html'
  success_url = reverse_lazy('accounts:login')
  
  def form_valid(self, form):
    form.instance.created_by = self.request.user
    logout(self.request)
    return super().form_valid(form)
  

class EnseignantCreateView( CreateView):
  model = Enseignant
  fields = ['nom', 'prenom', 'adresse', 'contact', 'email', 'photo', 'diplome', 'grade', 'spec']
  template_name = 'profil.html'
  success_url = reverse_lazy('accounts:login')
  
  def form_valid(self, form):
    form.instance.created_by = self.request.user
    logout(self.request)
    return super().form_valid(form)


class EvaluateurCreateView(CreateView ):
  model = Evaluateur
  fields = ['nom', 'prenom', 'email', 'contact', 'diplome', 'grade', 'spec']
  template_name = 'profil.html'
  success_url = reverse_lazy('accounts:login')

  def form_valid(self, form):
    form.instance.created_by = self.request.user
    logout(self.request)
    return super().form_valid(form)


@login_required
def create_profil(request:HttpRequest):
  if request.user.groups.filter(name='Evaluateur').exists():
    correct_view = EvaluateurCreateView.as_view()
  
  elif request.user.groups.filter(name='Enseignant').exists():
    correct_view = EnseignantCreateView.as_view()
  
  elif request.user.groups.filter(name='Ecole').exists():
    correct_view = EcoleCreateView.as_view()
  else:
    return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page", status=403)
  return correct_view(request)


@login_required
def profile(request:HttpRequest):
  if request.user.groups.filter(name='Evaluateur').exists():
    try:
      eva = get_object_or_404(Evaluateur, created_by=request.user)    
      return render(request, 'profiles/jury.html', context={'profil':eva}) 
    except:
      return render(request, 'profiles/jury.html') 
  
  elif request.user.groups.filter(name='Enseignant').exists():
    try:
      ens = get_object_or_404(Enseignant, created_by=request.user)
      return render(request, 'profiles/teacher.html', context={'profil':ens})
    except:
      return render(request, 'profiles/teacher.html' )
  
  elif request.user.groups.filter(name='Ecole').exists():
    try:
      eco = get_object_or_404(Ecole, created_by=request.user)
      return render(request, 'profiles/ecole.html', context={'profil':eco})
    except:
      return render(request, 'profiles/ecole.html' )






class CandidatureCreateView(PermissionRequiredMixin, CreateView):
  permission_required = ["recruit.view_enseignant", ]
  model = Candidature
  template_name = "candidater.html"
  fields = [ 'cv', 'demande', 'diplome', 'ifu', 'rib' ]
  success_url = reverse_lazy('recruit:stats')

  def get_context_data(self, **kwargs) :
    context = super().get_context_data(**kwargs)
    context["app"] = get_object_or_404(Appel, pk=self.kwargs['appel_id'])
    return context
  

  def form_valid(self, form):
    form.instance.enseignant = get_object_or_404(Enseignant, created_by=self.request.user)
    form.instance.appel = get_object_or_404(Appel, pk=self.kwargs['appel_id'])
    return super().form_valid(form)


class AppelCreateView(LoginRequiredMixin, CreateView):
    permission_required = "recruit.view_ecole"
    model = Appel
    form_class = AppelForm
    template_name = "lancer_appel.html"
    success_url = reverse_lazy('recruit:stats')

    def form_valid(self, form):
        # Associe l'école à l'instance avant de la sauvegarder
        form.instance.ecole = get_object_or_404(Ecole, created_by=self.request.user)
        # Sauvegarde l'instance et définit self.object
        self.object = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Si l'objet a été sauvegardé, on l'ajoute au contexte
        if hasattr(self, 'object'):
            context['object'] = self.object
        return context

    def post(self, request, *args, **kwargs):
        # Récupérer le formulaire
        form = self.get_form()

        # Si un fichier est envoyé, il sera pris en compte
        if 'document' in request.FILES:
            if form.is_valid():
                self.object = form.save()  # Sauvegarde l'instance
                return self.form_valid(form)  # Redirige vers la page de succès
            else:
                return self.form_invalid(form)  # Renvoie les erreurs si le formulaire est invalide
        else:
            return self.render_to_response(self.get_context_data(form=form))  # Sinon, on renvoie le formulaire avec erreurs éventuelles
  

class AppelUpdateView(UpdateView):
  model = Appel
  template_name = "modifier_appel.html"
  form_class = AppelForm
  success_url = reverse_lazy('recruit:stats')

  def post(self, request, *args, **kwargs):
        if 'document' in request.FILES:
            form = self.get_form()
            if form.is_valid():
                self.object = form.save()
                return self.form_valid(form)
            else:
                return self.form_invalid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))




class AppelDeleteView(DeleteView):
  model = Appel
  template_name = "del_appel.html"
  success_url = reverse_lazy('recruit:stats')


class AppelListView(ListView):
  model = Appel
  template_name = "appels.html"
  context_object_name = 'appels'
  def get_queryset(self):
    return super().get_queryset().filter(date_fin__gte=timezone.now())
  

class EvaluationCreateView(CreateView):
  model = Evaluation
  template_name = "evaluer.html"
  fields = [
            'haut_diplome',
            'grade',
            'spec',
            'departement',
            'ans_ecole',
            'ue_spec',
            'an_ens',
            'formation_justifie',
            'exp_entreprise',
            'age',
            'pieces',
            'decision',
            'observation',
            ]

  success_url = reverse_lazy('recruit:stats')

  def get_context_data(self, **kwargs)  :
    context = super().get_context_data(**kwargs)
    context["can"] = get_object_or_404(Candidature, pk=self.kwargs['candidature_id'])
    return context
  
  
  def form_valid(self, form):
    form.instance.evaluateur = get_object_or_404(Evaluateur, created_by=self.request.user)    
    cand = get_object_or_404(Candidature, pk=self.kwargs['candidature_id'])
    form.instance.candidature = cand
    cand.statut = 'fini'
    cand.save()
    return super().form_valid(form) 


class CandidatureListView(ListView):
  model = Candidature
  template_name = "candidature.html"
  context_object_name = 'cand'

  def get_queryset(self):
    appels = Appel.objects.filter(ecole=self.request.user.ecole)
    candidatures = Candidature.objects.filter(appel__in=appels).select_related('appel', 'enseignant')
    #return super().get_queryset().filter(appel__in=appels).select_related('appel', 'enseignant')  
    return candidatures
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    appels = Appel.objects.filter(ecole=self.request.user.ecole)
    context['appels'] = appels
    # Vérifie si chaque `can` a une évaluation associée avant d'appeler la méthode
    context['decisions'] = {
      appel.id: [
        eval_obj.get_decision_display() if (eval_obj := can.evaluation_set.first()) else "Non évalué"
        for can in Candidature.objects.filter(appel=appel)
      ]
      for appel in appels
    }
    return context


def candidater(request, appel_id):
    appel = get_object_or_404(Appel, id=appel_id)  # Récupère l'appel spécifique
    if request.method == 'POST':
        form = CandidatureForm(request.POST, request.FILES)
        if form.is_valid():
            candidature = form.save(commit=False)
            candidature.appel = appel  # Associe l'appel spécifique
            candidature.enseignant = request.user.enseignant  # Associe l'enseignant connecté
            candidature.save()
            return redirect('recruit:candidature_conf')  
    else:
        form = CandidatureForm()

    return render(request, 'candidater.html', {'form': form, 'app': appel})

def candidature_conf(request):
    return render(request, 'candidature_conf.html')


class EnseignantUpdateView(LoginRequiredMixin, UpdateView):
  model = Enseignant
  template_name = "up.html"
  fields = ['nom', 'prenom', 'adresse', 'contact', 'email', 'photo', 'diplome', 'grade', 'spec']
  success_url = reverse_lazy('recruit:profil')
  
  def get_object(self, queryset=None):
    return get_object_or_404(Enseignant, created_by=self.request.user)
  
 
class EvaluateurUpdateView(LoginRequiredMixin, UpdateView):
  model = Evaluateur
  template_name = "up.html"
  fields = ['nom', 'prenom', 'contact', 'email', 'diplome', 'grade', 'spec']
  success_url = reverse_lazy('recruit:profil')
  
  def get_object(self, queryset=None):
    return get_object_or_404(Evaluateur, created_by=self.request.user)
  

class EcoleUpdateView(UpdateView):
  model = Ecole
  template_name = "up.html"
  fields = ['nom', 'contact', 'email', 'adresse', 'photo', 'description']
  success_url = reverse_lazy('recruit:profil')
  
  def get_object(self, queryset=None):
    return get_object_or_404(Ecole, created_by=self.request.user)
  

@login_required
def update_profil(request:HttpRequest):
  if request.user.groups.filter(name='Evaluateur').exists():
    correct_view = EvaluateurUpdateView.as_view()
  
  elif request.user.groups.filter(name='Enseignant').exists():
    correct_view = EnseignantUpdateView.as_view()
  
  elif request.user.groups.filter(name='Ecole').exists():
    correct_view = EcoleUpdateView.as_view()
  else:
    return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page", status=403)
  return correct_view(request)



class CustomLoginView(LoginView):
    template_name = 'custom_login.html'

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Sauvegarder l'utilisateur
            user = form.save()

            # Obtenir le type d'utilisateur choisi
            user_type = form.cleaned_data['user_type']

            # Créer l'utilisateur en fonction du type
            if user_type == 'enseignant':
                enseignant = Enseignant.objects.create(
                    created_by=user,
                    nom=request.POST['nom'],
                    prenom=request.POST['prenom'],
                    email=request.POST['email'],
                    contact=request.POST['contact'],
                    adresse=request.POST['adresse'],
                    # Ajoute d'autres champs nécessaires ici
                )
            elif user_type == 'evaluateur':
                evaluateur = Evaluateur.objects.create(
                    created_by=user,
                    nom=request.POST['nom'],
                    prenom=request.POST['prenom'],
                    email=request.POST['email'],
                    contact=request.POST['contact'],
                    # Ajoute d'autres champs nécessaires ici
                )
            
            # Authentifier l'utilisateur et le connecter
            login(request, user)

            # Rediriger après l'inscription
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


# Dans ta vue
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['form_widget_types'] = {
        field.name: field.field.widget.__class__.__name__ for field in self.form
    }
    return context


@login_required
def redirect_dashboard(request):
    user = request.user
    
    # Déterminer le rôle de l'utilisateur
    if user.groups.filter(name="Enseignant").exists():
        role = "Enseignant"
    elif user.groups.filter(name="Ecole").exists():
        role = "Ecole"
    elif user.groups.filter(name="Evaluateur").exists():
        role = "Evaluateur"
    else:
        role = "Inconnu"

    return render(request, "dashboard.html", {"role": role})


def dashboard(request: HttpRequest):
    """
    Tableau de bord dynamique en fonction du rôle de l'utilisateur.
    """
    user = request.user

    # Si l'utilisateur est évaluateur
    if user.groups.filter(name="Evaluateur").exists():
        # Liste des candidatures en attente, triées par appel
        candidatures = Candidature.objects.filter(statut='attente').order_by("appel")
        context = {
            "title": "Candidatures en attente",
            "subtitle": "Liste des candidatures triées par appel",
            "candidatures": candidatures,
        }
        template_name = "stats/jury.html"

    # Si l'utilisateur est enseignant
    elif user.groups.filter(name="Enseignant").exists():
        candidatures = Candidature.objects.filter(enseignant=user.enseignant)
        evaluations = Evaluation.objects.filter(candidature__in=candidatures)
        context = {
            "title": "Vos Candidatures",
            "subtitle": "Candidatures soumises",
            "candidatures": candidatures,
            "decisions": [
                eva.get_decision_display() for eva in evaluations
            ],  # Décisions associées
        }
        template_name = "stats/teacher.html"

    # Si l'utilisateur est associé à une école
    elif user.groups.filter(name="Ecole").exists():
        # Liste des appels créés par l'école
        appels = Appel.objects.filter(ecole=user.ecole)
        candidatures = Candidature.objects.filter(appel__in=appels)  # Filtrage des candidatures par appel
        context = {
            "title": "Appels créés",
            "subtitle": "Candidatures soumises à vos appels",
            "candidatures": candidatures,
        }
        template_name = "stats/ecole.html"

    # Si l'utilisateur n'appartient à aucun groupe
    else:
        return HttpResponseForbidden("Vous n'êtes pas autorisé à accéder à cette page")

    # Afficher le tableau de bord correspondant
    return render(request, template_name, context)



def stats(request:HttpRequest):
    """
    Cette vue gère le contenu dynamique du dashboard en fonction des groupes d'utilisateur.
    """
    if request.user.groups.filter(name='Evaluateur').exists():
        # Liste des candidatures en attente, triées par appel
        candidatures = Candidature.objects.filter(statut='attente').order_by("appel")
        return render(request, 'stats/jury.html', context={'jury': candidatures, 'role': 'Evaluateur'})

    elif request.user.groups.filter(name='Enseignant').exists():
        # Liste des candidatures de l'enseignant
        candidatures = Candidature.objects.filter(enseignant=request.user.enseignant)
        evaluations = Evaluation.objects.filter(candidature__in=candidatures)
        
        # Liste des décisions pour chaque évaluation
        decisions = [eva.get_decision_display() for eva in evaluations]
        
        return render(request, 'stats/teacher.html', context={'candidatures': candidatures, 'decisions': decisions, 'role': 'Enseignant'})

    elif request.user.groups.filter(name='Ecole').exists():
        # Liste des appels créés par l'école
        appels = Appel.objects.filter(ecole=request.user.ecole)
        candidatures = Candidature.objects.filter(appel__in=appels)
        
        return render(request, 'stats/ecole.html', context={'appel': appels, 'candidatures': candidatures, 'role': 'Ecole'})

    # Si l'utilisateur ne fait partie d'aucun des groupes définis
    return HttpResponse("Vous n'êtes pas autorisé à accéder à cette page", status=403)

