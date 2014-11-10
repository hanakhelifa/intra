from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.thread, name='thread'),
    url(r'^thread/(?P<thread_id>\d+)/reply/$', views.reply, name='reply'),
)
