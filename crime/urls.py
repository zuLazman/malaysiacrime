from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
    url(r'show/(?P<id>\d+)/$', show, name='crime-show'),
    url(r'create/$', create, name='crime-create'),
    url(r'update/(?P<id>\d+)/$', update, name='crime-update'),
)
