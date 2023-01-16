from django import forms
from .models import Ticket, Review


RATING_CHOICES = [
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
]


class TicketForm(forms.ModelForm):
    """Form to create a ticket."""

    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    """Form to create a review."""

    rating = forms.TypedChoiceField(
        widget=forms.RadioSelect, choices=RATING_CHOICES, coerce=int
    )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
