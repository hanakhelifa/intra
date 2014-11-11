from forum.models import Post
from django import template

register = template.Library()
@register.filter(name='have_rights')
def have_rights(value, user):
    return value.have_rights(user)
