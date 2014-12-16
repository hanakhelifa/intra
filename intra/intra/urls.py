from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'intra.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
	url(r'^$', 'accueil.views.index', name='accueil'),
    url(r'^forum/', include('forum.urls', namespace='forum')),
	url(r'^tickets/', include('tickets.urls', namespace='tickets')),
)
