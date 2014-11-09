from django import template
from django.shortcuts import render

def index(request):
    render(request, 'forum/index.html', {'cat': None})

register = template.Library()
@register.inclusion_tag('forum/cat_list.html', name='cat_list')
def cat_list(cat):
    cat_list = cat.objects.filter(parent=cat).order_by('name')
    return {'cat_list': cat_list}
