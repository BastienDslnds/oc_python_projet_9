from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from . import models


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, label="Nom d'utilisateur")
    password = forms.CharField(
        max_length=30, widget=forms.PasswordInput, label="Mot de passe"
    )


class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = (
            get_user_model()
        )  # Pour récupérer le modèle User définit dans les settings AUTH_USER_MODEL
        fields = ('username',)
        help_texts = {'username': None}


class FollowUserForm(forms.ModelForm):
    add_subscription = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )

    class Meta:
        model = models.UserFollows
        fields = ['followed_user']


class UnfollowUserForm(forms.Form):
    delete_subscription = forms.BooleanField(
        widget=forms.HiddenInput, initial=True
    )
