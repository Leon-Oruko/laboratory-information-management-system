from django import forms
from core.models import Chemical, Microbio, Full

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields =  ('sample', 'analysis')

class MicrobioForm(forms.ModelForm):
    class Meta:
        model = Microbio
        fields =  ('sample', 'analysis')

class FullForm(forms.ModelForm):
    class Meta:
        model = Full
        fields =  ('sample', 'analysis')
