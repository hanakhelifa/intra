from forum.models import Category
from django import template

register = template.Library()
@register.inclusion_tag('forum/cat_list.html', name='cat_list')
def cat_list(cat):
    cat_list = Category.objects.filter(parent=cat).order_by('name')
    return {'cat_list': cat_list}
