from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
    url(r'^$', index, name='main-index'),
    url(r'^most/updated/$', most_updated, name='main-most-updated'),
)
