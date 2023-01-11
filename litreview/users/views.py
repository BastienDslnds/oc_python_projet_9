from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
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


@login_required
def logout_page(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)


@login_required
def subscriptions_page(request):
    follow_user_form = forms.FollowUserForm()
    unfollow_user_form = forms.UnfollowUserForm()
    subscriptions = models.UserFollows.objects.filter(user=request.user)
    subscribers = models.UserFollows.objects.filter(followed_user=request.user)
    print(request.POST)
    if request.method == 'POST':
        if 'add_subscription' in request.POST:
            follow_user_form = forms.FollowUserForm(request.POST)
            if follow_user_form.is_valid():
                userfollow = follow_user_form.save(commit=False)
                userfollow.user = request.user
                userfollow.save()
                return redirect('subscriptions')
        if 'delete_subscription' in request.POST:
            followed_user_id = request.POST.get('followed_user_id')
            followed_user = get_object_or_404(models.User, pk=followed_user_id)
            user_follow = models.UserFollows.objects.filter(
                user=request.user, followed_user=followed_user
            )
            user_follow.delete()
            return redirect('subscriptions')
    return render(
        request,
        "subscriptions.html",
        {
            'follow_user_form': follow_user_form,
            'unfollow_user_form': unfollow_user_form,
            'subscriptions': subscriptions,
            'subscribers': subscribers,
        },
    )
