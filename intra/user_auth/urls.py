from django.conf.urls import patterns, url
from register import views

urlpatterns = patterns('',
		url(r'^$', views.login_input, name='check_login'),
		url(r'^results/$', views.show_students, name='trombi'),
		url(r'^logout/$', views.user_logout, name='logout'),
)
