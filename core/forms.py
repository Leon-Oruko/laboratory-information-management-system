from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUsers

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUsers
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUsers
        fields = ("email",)




