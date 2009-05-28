from django.conf.urls.defaults import *
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.db.models import get_model
from django.views.generic.simple import direct_to_template

from views import *


crime_model = get_model('crime', 'crime')
crime_infodict = {'queryset': crime_model.objects.all(), 'date_field': 'updated_at'}
sitemaps = {'blog': GenericSitemap(crime_infodict)}

urlpatterns = patterns('',
    url(r'^$', index, name='main-index'),
    url(r'^recent/updated/$', recent_updated, name='main-recent-updated'),
    url(r'^recent/commented/$', recent_commented, name='main-recent-commented'),
    url(r'^search/$', direct_to_template, {'template': 'main/search.html'}, name='main-search'),
    url(r'^about/$', direct_to_template, {'template': 'main/about.html'}, name='main-about'),

    url(r'^icons.js$', direct_to_template, {'template': 'main/icons.js', 'mimetype': 'text/javascript'}, name='main-icons-js'),
    url(r'^robots.txt$', direct_to_template, {'template': 'main/robots.txt', 'mimetype': 'text/plain'}),
    url(r'^sitemap.xml$', sitemap, {'sitemaps': sitemaps}),
)
