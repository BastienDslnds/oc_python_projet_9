from django import forms
from .models import Ticket, Review


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')


class ReviewOnTicketForm(forms.ModelForm):
    # ticket champs masqué, placeholder au niveau du html default value
    # button value='id_ticket'

    class Meta:
        model = Review
        fields = ('headline', 'rating', 'body')
