from django import template
from forum.models import Category, Post

register = template.Library()

@register.inclusion_tag('forum/cat_list.html', name='cat_list')
def cat_list(cat):
    cat_list = Category.objects.filter(parent=cat).order_by('name')
    return {'cat_list': cat_list}

@register.filter(name='have_rights')
def have_rights(value, user):
    return value.have_rights(user)

@register.filter(name='can_reply')
def can_reply(value):
    return value.is_post()
