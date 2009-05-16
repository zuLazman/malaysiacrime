from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
    url(r'^$', index, name='main-index'),
    url(r'^recent/updated/$', recent_updated, name='main-recent-updated'),
)
