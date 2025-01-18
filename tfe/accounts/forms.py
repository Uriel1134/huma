from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Adresse e-mail")  # Ajout du champ email
    group_choices = [
        ('Ecole', 'Ecole'),
        ('Enseignant', 'Enseignant'),
        ('Evaluateur', 'Evaluateur'),
    ]
    groups = forms.ChoiceField(choices=group_choices, required=True, label="Type d'utilisateur")

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'groups')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            # Assigner l'utilisateur au groupe choisi
            group_name = self.cleaned_data['groups']
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        return user

  # def clean_groups(self):
  #   group = self.cleaned_data.get("groups")
  #   if (group.count() > 1 or group.count() < 1 ):
  #     raise forms.ValidationError('Sélectionner une catégorie')
  #   return group
  

