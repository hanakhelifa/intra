from django import template
from forum.models import Category, Post
from forum.utils import custom_set

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
    return not value.is_comment()

@register.filter(name='posts_list')
def list_posts(thread):
    return custom_set(Post.thread.get_thread(thread).order_by('id'))

@register.filter(name='comments_list')
def list_comments(post):
    return custom_set(Post.thread.get_comment_thread(post).order_by('id')[1:])
