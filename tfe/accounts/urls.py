from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView

app_name = "accounts"
urlpatterns = [
  path("signup/", views.signup, name="signup"),
  path("login/", LoginView.as_view(template_name='login.html'), name="login"),
  path("logout/", views.logouts, name="logout"),
  path("modifier_password/", PasswordChangeView.as_view(template_name='password.html', success_url = reverse_lazy("recruit:dash")), name="change_pwd"),
]
