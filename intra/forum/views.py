from django import forms
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forum.models import Post, Category

@login_required
def index(request):
    return render(request, 'forum/index.html', {'cat': None})

@login_required
def thread(request, thread_id):
    try:
        thread = Post.objects.get(id=thread_id)
        if not thread.is_thread() and not thread.is_post():
            raise Http404
    except ObjectDoesNotExist:
        raise Http404
    posts = Post.thread.get_thread(thread).order_by('id')
    old_post = request.session.get('_old_post')
    if old_post:
        del request.session['_old_post']
    post = Post(cat=thread.cat, parent=thread, author=request.user)
    form = PostForm(old_post, instance=post)
    tmp_thread = thread
    while not (tmp_thread.parent is None):
        tmp_thread = tmp_thread.parent
    context = {
        'thread': thread,
        'posts': posts,
        'form': form,
        'thread_title': tmp_thread.title,
    }
    return render(request, 'forum/thread.html', context)

@login_required
def reply(request, thread_id):
    thread = get_object_or_404(Post, id=thread_id)
    if not thread.is_thread() and not thread.is_post():
        raise Http404
    post = Post(cat=thread.cat, parent=thread, author=request.user)
    if request.method == 'POST':
        request.session['_old_post'] = request.POST
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            del request.session['_old_post']
            form.save()
            return HttpResponseRedirect(reverse(
                'forum:thread',
                args=[thread_id]
            ))
    return HttpResponseRedirect(reverse('forum:thread', args=[thread_id]))

@login_required
def category(request, cat_id):
    cat = get_object_or_404(Category, id=cat_id)
    threads = Post.objects.filter(cat=cat, parent=None)
    context = {
        'cat': cat,
        'threads': threads,
    }
    return render(request, 'forum/category.html', context)

@login_required
def new_thread(request, cat_id):
    cat = get_object_or_404(Category, id=cat_id)
    thread = Post(cat=cat, parent=None, author=request.user)
    if request.method == "POST":
        form = ThreadForm(request.POST, instance=thread)
        if form.is_valid():
            thread = form.save()
            return HttpResponseRedirect(reverse(
                'forum:thread',
                args=[thread.id]
            ))
    else:
        form = ThreadForm(instance=thread)
    context = {
        'cat': cat,
        'form': form,
    }
    return render(request, 'forum/new_thread.html', context)

@login_required
def edit_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if not post.have_rights(request.user):
            raise Http404
        if post.is_thread():
            thread = post
        elif post.parent.is_thread():
            thread = post.parent
        elif post.parent.parent.is_thread():
            thread = post.parent.parent
    except ObjectDoesNotExist:
        raise Http404
    posts = (Post.thread.get_thread(thread)
        .filter(id__lt=post.id)
        .order_by('-id')
        [:5]
    )
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse(
                'forum:thread',
                args=[thread.id]
            ))
    else:
        form = PostForm(initial={'message': post.message}, instance=post)
    context = {
        'thread': thread,
        'posts': posts,
        'form': form,
        'post': post,
    }
    return render(request, 'forum/edit_post.html', context)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message']
