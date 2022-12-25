from django import template

# from litreview.review.models import Ticket

register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_review_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


# @register.simple_tag(takes_context=True)
# def ticket_already_with_review(context):
#     """Vérifier si le user a créé une review sur le ticket.
#     Vérifier s'il y a un ticket avec le user dans la table Review.
#     """
#     if Ticket.objects.filter(review__user=context['user']):
#         return True
#     return False
