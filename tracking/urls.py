from django.conf.urls import patterns, url

urlpatterns = patterns('tracking.views',
    url(r'^$', 'dashboard', name='tracking-dashboard'),
    url(r'^dashboard/$', 'stats'),
    url(r'^session/(?P<session_id>.*?)/$', 'session'),
)
