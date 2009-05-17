from django.conf.urls.defaults import *
from django.contrib.sitemaps import GenericSitemap
from django.db.models import get_model

from views import *


crime_model = get_model('crime', 'crime')
crime_infodict = {'queryset': crime_model.objects.all(), 'date_field': 'updated_at'}
sitemaps = {'blog': GenericSitemap(crime_infodict)}

urlpatterns = patterns('',
    url(r'^$', index, name='main-index'),
    url(r'^recent/updated/$', recent_updated, name='main-recent-updated'),
    url(r'^recent/commented/$', recent_commented, name='main-recent-commented'),

    url(r'^sitemap.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': sitemaps}),
)
