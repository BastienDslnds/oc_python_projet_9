from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Ticket, Review
from itertools import chain
from . import forms


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
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


@login_required
def change_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    form = forms.TicketForm(instance=ticket)
    if request.method == 'POST':
        form = forms.TicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(request, "change_ticket.html", {'form': form})


@login_required
def change_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    ticket = review.ticket
    form = forms.ReviewForm(instance=review)
    if request.method == 'POST':
        form = forms.ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('posts')
    return render(
        request, "change_review.html", {'ticket': ticket, 'form': form}
    )


@login_required
def delete_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        ticket.delete()
        return redirect('posts')
    return render(request, "delete_ticket.html", {'ticket': ticket})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if request.method == 'POST':
        review.delete()
        return redirect('posts')
    return render(request, "delete_review.html", {'review': review})
