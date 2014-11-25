from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from ldap3 import Server, Connectionm STARTEGY_SYNC, SEARCH_SCOPE_WHOLE_SUBTREE

def user_login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect(reverse("page d'accueuil"))
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			form_data = form.cleaned_data
			user = authenticate(username=form_data['username'], password=form_data['password'])
			if user is not None:
				if user.is_active:
					login(request, user)
					return HttpResponseRedirect(reverse('helloworld'))
				else:
					return HttpResponse('disabled account')
			else:
				return HttpResponse('invalid login')
	else:
		form = AuthenticationForm()
	return render(request, 'register/register_form.html', { 'form' : form })

def user_logout(request):
	logout(request)
	return HttpResponseRedirect(reverse('homepage'))

def	login_input(request):
	return render(request, 'trombi/request_login.html')

def show_students(request):
	today = datetime.date.today()
	year = today.year
	base_dn = "ou=people,dc=42,dc=fr"
	scope = SEARCH_SCOPE_WHOLE_SUBTREE
	filtre = '(&(objectClass=ft-user)(dc:dn:=42)(dc:dn:=fr)(|(ou:dn:=2013)(ou:dn:=2014))(ou:dn:=people)(&(!(close=non-admis))(!(close=non admis))))'
	attrs = ['cn','uid', 'birth-date','mobile-phone', 'picture']
	s = Server('ldaps://ldap.42.fr:636')
	uid = request.POST['username']
	pwd = request.POST['password']
#	if request.user.is_authenticated():
#		c = Connection(s, user=dn, password=pw, auto_bind=True)
#		return HttpResponseRedirect(reverse('trombi'))
	if request.method == 'POST':
		#		form = AuthenticationForm(data=request.POST)
#		if form.is_valid():
#			form_data = form.cleaned_data
#			user = authenticate(username=username, password=pwd)
			for y in range(2013, year + 1):
				user = Connection(s, client_strategy=STRATEGY_SYNC, user=uid, password=pwd, auto_bind=True, authentication=AUTH_SIMPLE)
				dn = {'uid':{% uid %}, 'ou':{% ou %}, 'ou':people, 'dc':42, 'dc':fr}
				except:
#					user = authenticate(username=form_data['username'], password=form_data['password'])
			if user is not None:
#				if user.is_active:
#				c = Connection(s, user=username, password=pwd, auto_bind=True)
				login(request, user)
				return HttpResponseRedirect(reverse('trombi'))
			else:
				return render(request, 'trombi/login_error.html')
#				return HttpResponseRedirect(reverse('check_login'))
	c.search(base_dn, filtre, scope, attributes = attrs)
	students = []
	for entry in c.response:
		student = []
		if 'cn' in entry["attributes"]:
			student.append(entry["attributes"]["cn"])
		else:
			student.append([])
#		if 'uid' in entry["attributes"]:
#			student.append(entry["attributes"]["uid"])
#		else:
#			student.append([])
#		if 'picture' in entry["raw_attributes"]:
#			student.append([base64.b64encode(entry["raw_attributes"]["picture"][0])])
#		else:
#			student.append(["http://i.imgur.com/jYVMSjJ.gif"])
		students.append(student)
	context = {"toto":students}
	return render(request, 'trombi/aff_student.html', context)
