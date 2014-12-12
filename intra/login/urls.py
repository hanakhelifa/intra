from django.conf.urls import patterns, url
from login import views

urlpatterns = patterns('',
		url(r'^$', views.user_login, name='login'),
		url(r'^logout/$', views.user_logout, name='logout'),
)
