from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Ticket, Review
from users.models import UserFollows, User
from itertools import chain
from . import forms
from django.db.models import Q


@login_required
def feed(request):
    """View with latest tickets and reviews
    from the user authenticated and his followed users.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    followed_user = UserFollows.objects.filter(user=request.user)
    followed_user = [user.followed_user for user in followed_user]
    tickets = Ticket.objects.filter(
        Q(user=request.user) | Q(user__in=followed_user)
    )
    reviews = Review.objects.filter(
        Q(user=request.user)
        | Q(ticket__user=request.user)
        | Q(user__in=followed_user)
    )
    tickets_already_with_review = {}
    for ticket in tickets:
        key = f"{ticket.pk}"
        if (
            ticket in Ticket.objects.filter(review__user=request.user)
            or ticket.user == request.user
        ):
            tickets_already_with_review[key] = True
        else:
            tickets_already_with_review[key] = False
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response = render(
        request,
        "feed.html",
        {
            'tickets_already_with_review': tickets_already_with_review,
            'page_obj': page_obj,
        },
    )

    return response


@login_required
def posts(request):
    """View with tickets and reviews from the authenticated user.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )

    paginator = Paginator(tickets_and_reviews, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    response = render(request, "posts.html", {'page_obj': page_obj})
    return response


@login_required
def add_review(request):
    """View to add a ticket and a an associated review.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    review_form = forms.ReviewForm()
    ticket_form = forms.TicketForm()
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        ticket_form = forms.TicketForm(request.POST, request.FILES)
        if all((review_form.is_valid(), ticket_form.is_valid())):
            ticket = ticket_form.save(commit=False)
            ticket.user = request.user
            ticket.save()
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    response = render(
        request,
        "create_review.html",
        {'review_form': review_form, 'ticket_form': ticket_form},
    )
    return response


@login_required
def add_review_to_ticket(request, ticket_id):
    """View to add a review in response of an existing ticket.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    review_form = forms.ReviewForm()
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        review_form = forms.ReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    response = render(
        request,
        "create_review_to_ticket.html",
        {'ticket': ticket, 'form': review_form},
    )
    return response


@login_required
def add_ticket(request):
    """View to add a ticket.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            print(ticket)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    response = render(request, "create_ticket.html", {'form': form})
    return response


@login_required
def change_ticket(request, ticket_id):
    """View to modify a ticket.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    response = render(request, "change_ticket.html", {'form': form})
    return response


@login_required
def change_review(request, review_id):
    """View to modify a review.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    review = get_object_or_404(Review, pk=review_id)
    ticket = review.ticket
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    response = render(
        request, "change_review.html", {'ticket': ticket, 'form': form}
    )
    return response


@login_required
def delete_ticket(request, ticket_id):
    """View to delete a ticket.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    response = render(request, "delete_ticket.html", {'ticket': ticket})
    return response


@login_required
def delete_review(request, review_id):
    """View to delete a review.

    Args:
        request (django.core.handlers.wsgi.WSGIRequest): request

    Returns:
       response (django.http.response.HttpResponse): response to the request
    """
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    response = render(request, "delete_review.html", {'review': review})
    return response
