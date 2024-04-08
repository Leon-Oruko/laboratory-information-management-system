from django import forms
from core.models import Chemical, Microbio, Full

class ChemicalForm(forms.ModelForm):
    class Meta:
        model = Chemical
        fields = '__all__'

class MicrobioForm(forms.ModelForm):
    class Meta:
        model = Microbio
        fields = '__all__'

class FullForm(forms.ModelForm):
    class Meta:
        model = Full
        fields = '__all__'
