from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms
from . import models


def login_page(request):
    form = forms.LoginForm()
    message = ''
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                login(request, user)
                return redirect('feed')
            else:
                message = 'Identifiants invalides'
    return render(
        request, "home.html", context={'form': form, 'message': message}
    )


def signup_page(request):
    form = forms.SignupForm()
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(settings.LOGIN_REDIRECT_URL)
    return render(request, "signup.html", {'form': form})


def logout_page(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


def subscriptions_page(request):
    form = forms.FollowUserForm()
    if request.method == 'POST':
        form = forms.FollowUserForm(request.POST)
        if form.is_valid():
            userfollow = form.save(commit=False)
            userfollow.user = request.user
            userfollow.save()
            return redirect('subscriptions')
    return render(request, "subscriptions.html", {'form': form})
