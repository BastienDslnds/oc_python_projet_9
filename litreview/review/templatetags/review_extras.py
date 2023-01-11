from django import template


register = template.Library()


@register.filter
def model_type(value):
    return type(value).__name__


@register.simple_tag(takes_context=True)
def get_review_display(context, user):
    if user == context['user']:
        return 'vous'
    return user.username


@register.filter
def review_done(dictionary, key):
    return dictionary.get(str(key))
