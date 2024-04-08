# create form for user registeration
from django import forms
from core.models import CustomUsers
class UserRegisterationForm(forms.ModelForm):
    class Meta:
        model = CustomUsers
        fields = ['username','email', 'password' ,'post']

    def clean_sample_id(self):
        # Add any custom validation logic for sample_id field
        username = self.cleaned_data['username']
        # Example: Check if the sample_id already exists in the database
        if CustomUsers.objects.filter(username=username).exists():
            raise forms.ValidationError("Sample ID already exists.")
        return username

