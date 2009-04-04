from django.conf.urls.defaults import *

from views import *


urlpatterns = patterns('',
    url(r'^$', index, name='main-index'),
)
