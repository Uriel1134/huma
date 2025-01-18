from django.urls import path
from django.conf.urls.static import static

from tfe import settings
from . import views
from .views import *


app_name = "recruit"
urlpatterns = [
  path("accueil/", views.accueil, name="home"),
  path("create_profil/", views.create_profil, name="profil_creation"),
  path("appels/", AppelListView.as_view(), name="appels"),
  path("profil/", views.profile, name="profil"),
  path("demandes/", views.stats, name="stats"),
  path("dash/", views.dash, name="dash"),
  path("postuler/<int:appel_id>/", CandidatureCreateView.as_view(), name="candidater"),
  path("lancer_appel/", AppelCreateView.as_view(), name="lancer_appel"),
  path("evaluer/<int:candidature_id>/", EvaluationCreateView.as_view(), name="evaluer"),
  path("candidatures/", CandidatureListView.as_view(), name="candidatures"),
  path("modifier_appel/<int:pk>", AppelUpdateView.as_view(), name="up_appel"),
  path("supprimer_appel/<int:pk>", AppelDeleteView.as_view(), name="del_appel"),
  path("up/", views.update_profil, name="update"),
  path('candidater/<int:appel_id>/', views.candidater, name='candidater'),
  path('candidature_conf/', views.candidature_conf, name='candidature_conf'),
  path('login/', CustomLoginView.as_view(), name='login'),
  path('signup/', signup_view, name='signup'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

