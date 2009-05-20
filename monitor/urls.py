from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from views import *


urlpatterns = patterns('',
    url(r'subscribe/$', subscribe, name='monitor-subscribe'),
    url(r'subscribe/done/$', subscribe_done, name='monitor-subscribe-done'),

)
