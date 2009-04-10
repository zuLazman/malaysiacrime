from django.db import models
from django.utils.translation import ugettext as _


class Crime(models.Model):
    """
    Represents a crime report.
    """
    headline   = models.CharField(max_length=100)
    date       = models.DateField()
    location   = models.CharField(max_length=300)
    lat        = models.FloatField()
    lng        = models.FloatField()
    details    = models.TextField()
    password   = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
