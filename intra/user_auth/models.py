from django.db import models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, BaseUserManager, AbstractBaseUser
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

class MyManager(BaseUserManager):
	def create_user(self, uid, password=None):
		if not uid:
			raise ValueError ("User must have valid uid")
		user = self.model(uid=uid)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, uid, password):
		user = self.create_user(email, password)
		user.is_admin=True
		user.save(using=self._db)
		return user

class MyUser(AbstractBaseUser):
	uid = models.CharField(max_length=8, unique=True, primary_key=True)
	pwd = models.CharField(max_length=20)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	birth_date = models.DateField(auto_now=False, auto_now_add=False)
	promo = models.ForeignKey('Promo')
	USERNAME_FIELD = 'uid'

	objects = MyManager()

	def get_full_name(self):
		return self.uid

	def get_short_name(self):
		return self.uid

	def user_login(request):
		if request.uid.is_authenticated():
			return HttpResponse('user authenticated')
		if request.method == 'POST':
			form = AuthenticationForm(data=request.POST)
			if form.is_valid():
				 uid = authenticate(username=form_data['uid'], password=form_data['pwd'])
				 if uid is not None:
					 if uid.is_active:
						 login(request, uid)
						 return HttpResponse('user logged in')
					 else:
						 return HttpResponse('disabled account')
			else:
				return HttpResponse('user does not exist')
		else:
			form = AuthenticationForm()
		return HttpResponse('congratulations, you have been accepted!')


class Promo(models.Model):
	year = models.CharField(max_length=4)



