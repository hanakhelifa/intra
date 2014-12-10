from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

def user_login(request):
	if request.user.is_authenticated():
		return HttpResponse('User logged in')
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			user = authenticate(username=form_data['username'], password=form_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('admin:index'))
				else:
					return HttpResponse('disabled account')
			else:
				return HttpResponse('invalid login')
	else:
		form = AuthenticationForm()
	return render(request, 'login/login.html', { 'form' : form })

def user_logout(request):
	logout(request)
	return HttpResponse('User logged out')

