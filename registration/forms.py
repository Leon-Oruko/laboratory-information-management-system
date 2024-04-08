# forms.py
from django import forms
from core.models import Sample,Clients
from django.forms.widgets import Select
class SampleRegistrationForm(forms.ModelForm):
    class Meta:
        model = Sample
        fields = ['sample_id', 'sample_name', 'test_id', 'customer']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['customer'].widget = CustomDropdownWithButtonWidget()

    def clean_sample_id(self):
        # Add any custom validation logic for sample_id field
        sample_id = self.cleaned_data['sample_id']
        # Example: Check if the sample_id already exists in the database
        if Sample.objects.filter(sample_id=sample_id).exists():
            raise forms.ValidationError("Sample ID already exists.")
        return sample_id
    


# class CustomDropdownWithButtonWidget(Select):
#     template_name = 'registration/custom_dropdown_with_button.html'

class ClientRegisterationForm(forms.ModelForm):
    class Meta:
        model=Clients
        fields='__all__'

