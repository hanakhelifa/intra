from django.conf.urls import patterns, url
from homepage import views

urlpatterns = patterns('',
		url(r'^$', views.show_homepage, name='homepage'),
)
