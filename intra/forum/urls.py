from django.conf.urls import patterns, url
from forum import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.thread, name='thread'),
    url(r'^thread/(?P<thread_id>\d+)/reply/$', views.reply, name='reply'),
    url(r'^category/(?P<cat_id>\d+)/$', views.category, name='category'),
    url(
        r'^category/(?P<cat_id>\d+)/new/$',
        views.new_thread,
        name='new_thread'
    ),
    url(r'^post/(?P<post_id>\d+)/edit/$', views.edit_post, name='edit_post'),
)
