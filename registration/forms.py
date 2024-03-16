# forms.py
from django import forms
from core.models import Sample

class SampleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sample_id', 'sample_name', 'sample_type', 'industry_type']

    def clean_sample_id(self):
        # Add any custom validation logic for sample_id field
        sample_id = self.cleaned_data['sample_id']
        # Example: Check if the sample_id already exists in the database
        if Sample.objects.filter(sample_id=sample_id).exists():
            raise forms.ValidationError("Sample ID already exists.")
        return sample_id