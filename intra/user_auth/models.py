from django.db import models

class User(models.Model):
	uid = models.CharField(max_length=8)
	password = models.CharField(max_length=20)
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	birth_date = models.DateField(auto_now=False, auto_now_add=False)
	promo = models.ForeignKey('Promo')
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
#	is_ldap

class Promo(models.Model):
	year = models.CharField(max_length=4)
