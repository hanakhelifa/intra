from django import forms
from django.contrib.auth.decorators import login_required
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
        if not thread.is_thread():
            raise Http404
    except:
        raise Http404
    old_post = request.session.get('_old_post')
    if old_post:
        del request.session['_old_post']
    post = Post(cat=thread.cat, parent=thread, author=request.user)
    form = PostForm(old_post, instance=post)
    context = {
        'thread': thread,
        'form': form,
    }
    return render(request, 'forum/thread.html', context)

@login_required
def reply(request, thread_id):
    thread = get_object_or_404(Post, id=thread_id)
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
    try:
        cat = Category.objects.get(id=cat_id)
    except:
        raise Http404
    threads = Post.objects.filter(cat=cat, parent=None)
    context = {
        'cat': cat,
        'threads': threads,
    }
    return render(request, 'forum/category.html', context)

@login_required
def new_thread(request, cat_id):
    try:
        cat = Category.objects.get(id=cat_id)
    except:
        raise Http404
    thread = Post(cat=cat, parent=None, author=request.user)
    if request.method == "POST":
        form = PostForm(request.POST, instance=thread)
        if form.is_valid():
            thread = form.save()
            return HttpResponseRedirect(reverse(
                'forum:thread',
                args=[thread.id]
            ))
    else:
        form = PostForm(instance=thread)
    context = {
        'cat': cat,
        'form': form,
    }
    return render(request, 'forum/new_thread.html', context)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message']
