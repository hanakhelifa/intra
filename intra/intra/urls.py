from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^user/', include('auth.urls', namespace='auth')),
)
