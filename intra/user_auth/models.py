from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

class User(AbstractBaseUser):
	uid = models.CharField(max_length=8, unique=True, primary_key=True)
	password = models.CharField(max_length=20)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	birth_date = models.DateField(auto_now=False, auto_now_add=False)
	promo = models.ForeignKey('Promo')
	USERNAME_FIELD = 'uid'
	REQUIRED_FIELDS = ['first_name', 'last_name', 'birth_date', 'promo']

	def user_login(request):
		if request.uid.is_authenticated():
			return HttpResponse('user authenticated')
		if request.method == 'POST':
			form = AuthenticationForm(data=request.POST)
			if form.is_valid():
				 uid = authenticate(username=form_data['uid'], password=form_data['password'])



class Promo(models.Model):
	year = models.CharField(max_length=4)



