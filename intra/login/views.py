from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from ldap import Server, Connection, STRATEGY_SYNC, SEARCH_SCOPE_WHOLE_TREE, GET_ALL_INFO, AUTH_SIMPLE

def user_login(request):
	s = Server('ldaps://ldap.42.fr:636')
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
				c = Connection(s, client_strategy=STRATEGY_SYNC, auto_bind=True, authentication=AUTH_SIMPLE)
				return render ('USE LDAP')
	else:
		form = AuthenticationForm()
	return render(request, 'login/login.html', { 'form' : form })

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('login'))	

