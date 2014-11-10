from django import forms
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from forum.models import Post

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
    form = ReplyForm(old_post)
    context = {
        'thread': thread,
        'form': form,
    }
    return render(request, 'forum/thread.html', context)

@login_required
def reply(request, thread_id):
    thread = get_object_or_404(Post, id=thread_id)
    if request.method == 'POST':
        old_post = request.session['_old_post']
        del request.session['_old_post']
        form = ReplyForm(old_post or None)
        form.cat = thread.cat
        form.parent = thread
        form.author = request.user
        form.title = None
        if form.is_valid():
            return HttpResponse('Ok')
    return HttpResponseRedirect(reverse('forum:thread', args=[thread_id]))

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'message']
