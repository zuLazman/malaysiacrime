from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import *


urlpatterns = patterns('',
    url(r'^subscribe/$', subscribe, name='monitor-subscribe'),
    url(r'^subscribe/done/(?P<uuid>[\w\d]{32})/$', subscribe_done, name='monitor-subscribe-done'),
    url(r'^subscribe/confirm/(?P<uuid>[\w\d]{32})/$', subscribe_confirm, name='monitor-subscribe-confirm'),

    url(r'^unsubscribe/done/(?P<uuid>[\w\d]{32})/$', unsubscribe_done, name='monitor-unsubscribe-done'),
    url(r'^unsubscribe/confirm/(?P<uuid>[\w\d]{32})/$', unsubscribe_confirm, name='monitor-unsubscribe-confirm'),

    url(r'^area/(?P<uuid>[\w\d]{32})/$', area, name='monitor-area'),
)
