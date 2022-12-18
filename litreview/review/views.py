from django.shortcuts import render, get_object_or_404
from .models import Ticket, Review


def feed(request):
    """View with latest tickets and reviews from users followed.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    latest_reviews_list = Review.objects.order_by('-time_created')
    latest_tickets_list = Ticket.objects.order_by('-time_created')
    #  Comment créer une liste pour regrouper les 2 ?
    return render(request, "feed.html", {'latest_list': latest_list})


def posts(request):
    """View with our own tickets and reviews.

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    latest_reviews_list = Review.objects.order_by('-time_created')
    latest_tickets_list = Ticket.objects.order_by('-time_created')
    return render(request, "posts.html")


def add_review(request):
    return render(request, "create_review.html")


def add_review_to_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    return render(request, "create_review_to_ticket.html", {'ticket': ticket})


def add_ticket(request):
    return render(request, "create_ticket.html")


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
