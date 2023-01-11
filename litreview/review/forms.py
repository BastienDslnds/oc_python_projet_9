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
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    rating = forms.TypedChoiceField(
        widget=forms.RadioSelect, choices=RATING_CHOICES, coerce=int
    )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')


class ReviewOnTicketForm(forms.ModelForm):
    # ticket champs masqué, placeholder au niveau du html default value
    # button value='id_ticket'
    rating = forms.TypedChoiceField(
        widget=forms.RadioSelect, choices=RATING_CHOICES, coerce=int
    )

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
