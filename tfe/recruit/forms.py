from django import forms
from .models import *

class AppelForm(forms.ModelForm):
  
  class Meta:
    model = Appel     
    fields = '__all__'
    widgets = {
      "date_fin" : forms.DateInput(attrs={"type":"date"}),
      'document': forms.ClearableFileInput(attrs={'class': 'form-control'})
    }

    # RangeWidget(base_widget=)


class EnseignantForm(forms.ModelForm):
    class Meta:
        model = Enseignant
        fields = ['nom', 'prenom', 'diplome', 'grade', 'spec']

    def clean_diplome(self):
        diplome = self.cleaned_data.get('diplome')
        if not diplome:
            raise forms.ValidationError("Le diplôme est requis.")
        return diplome

    def clean_grade(self):
        grade = self.cleaned_data.get('grade')
        if not grade:
            raise forms.ValidationError("Le grade est requis.")
        return grade

    def clean_spec(self):
        spec = self.cleaned_data.get('spec')
        if not spec:
            raise forms.ValidationError("La spécialité est requise.")
        return spec


class CandidatureForm(forms.ModelForm):
    class Meta:
        model = Candidature
        fields = ['cv', 'demande', 'diplome', 'ifu', 'rib', 'autre']  # Adapté à vos champs de fichier

    def __init__(self, *args, **kwargs):
        super(CandidatureForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})