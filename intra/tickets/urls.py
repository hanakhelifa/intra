from django.conf.urls import patterns, url
from tickets import views

urlpatterns = patterns('',
    url(r'^pool/$', views.pool, name='pool'),
    url(r'^$', views.tickets_list, name='list'),
    url(r'^new/$', views.create, name='create'),
    url(r'^view/(?P<ticket_id>\d+)/$', views.view, name='view'),
)
