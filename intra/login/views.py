import ldap
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from user_auth.models import MyUser

def user_login(request):
	uid = request.POST['username']
	pwd = request.POST['password']
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse('homepage'))
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			user = authenticate(username=form_data['username'], password=form_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('homepage'))
				else:
					return HttpResponse('disabled account')
			else:
				init = ldap.initialize('ldaps://ldap.42.fr:636')
				init.simple_bind(uid,pwd) 
				return HttpResponseRedirect(reverse('homepage'))
			#	return render ('USE LDAP')
	else:
		form = AuthenticationForm()
	return render(request, 'login/login.html', { 'form' : form })

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))	

