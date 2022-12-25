from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Review
from itertools import chain
from . import forms


def feed(request):
    """View with latest tickets and reviews from users followed.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    return render(
        request, "feed.html", {'tickets_and_reviews': tickets_and_reviews}
    )


def posts(request):
    """View with our own tickets and reviews.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    tickets = Ticket.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    tickets_and_reviews = sorted(
        chain(tickets, reviews),
        key=lambda instance: instance.time_created,
        reverse=True,
    )
    return render(
        request, "posts.html", {'tickets_and_reviews': tickets_and_reviews}
    )


def add_review(request):
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
    return render(
        request,
        "create_review.html",
        {'review_form': review_form, 'ticket_form': ticket_form},
    )


def add_review_to_ticket(request, ticket_id):
    review_form = forms.ReviewOnTicketForm()
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        review_form = forms.ReviewOnTicketForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()
            return redirect('feed')
    return render(
        request,
        "create_review_to_ticket.html",
        {'ticket': ticket, 'form': review_form},
    )


def add_ticket(request):
    form = forms.TicketForm()
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, request.FILES)
        if form.is_valid():
            ticket = form.save(commit=False)
            print(ticket)
            ticket.user = request.user
            ticket.save()
            return redirect('feed')
    return render(request, "create_ticket.html", {'form': form})


def change_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, "change_ticket.html", {'ticket': ticket})


def change_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, "change_review.html", {'review': review})


def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, "delete_ticket.html", {'ticket': ticket})


def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    return render(request, "delete_review.html", {'review': review})
