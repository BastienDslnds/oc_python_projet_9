from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket, Review
from . import forms


def feed(request):
    """View with latest tickets and reviews from users followed.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # latest_reviews_list = Review.objects.order_by('-time_created')
    # latest_tickets_list = Ticket.objects.order_by('-time_created')
    # Comment créer une liste pour regrouper les 2 ?
    tickets = Ticket.objects.all()
    reviews = Review.objects.all()
    return render(
        request, "feed.html", {'tickets': tickets, 'reviews': reviews}
    )


def posts(request):
    """View with our own tickets and reviews.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    # latest_reviews_list = Review.objects.order_by('-time_created')
    # latest_tickets_list = Ticket.objects.order_by('-time_created')
    return render(request, "posts.html")


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
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, "create_review_to_ticket.html", {'ticket': ticket})


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
