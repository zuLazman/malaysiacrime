from django.db import models
from django.utils.translation import ugettext as _


class Crime(models.Model):
    """
    Represents a crime report.
    """
    headline   = models.CharField(max_length=100)
    date       = models.DateField()
    location   = models.CharField(max_length=300)
    icon       = models.CharField(max_length=50)
    lat        = models.FloatField()
    lng        = models.FloatField()
    zoom       = models.IntegerField()
    details    = models.TextField()
    author     = models.CharField(max_length=50)
    password   = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.headline

    @models.permalink
    def get_absolute_url(self):
        return ('crime-show', (), {'id': self.id})
