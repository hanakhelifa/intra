from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
   	url(r'^login/', include('login.urls')),
    url(r'^admin/', include(admin.site.urls)),
   	url(r'^homepage/', include('homepage.urls')),
)
