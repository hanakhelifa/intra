from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^user/', include('intra_auth.urls', namespace='auth')),
)
