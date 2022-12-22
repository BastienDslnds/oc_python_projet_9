from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(
        max_length=30, widget=forms.PasswordInput, label="mot de passe"
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = (
            get_user_model()
        )  # Pour récupérer le modèle User définit dans les settings AUTH_USER_MODEL
        fields = ('username',)


class FollowUserForm(forms.Form):
    # il faut relié à un user via foreignkey ?
    pass
