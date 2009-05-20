from django.db import models

class Moniton(models.Model):
    """
    A monitoring unit. Consist of the monitored area and email.
    """
    email      = models.EmailField()
    north      = models.FloatField()
    east       = models.FloatField()
    south      = models.FloatField()
    west       = models.FloatField()
    registered = models.BooleanField(default=False)
    add_uuid   = models.CharField(max_length=32, default='', blank=True)
    del_uuid   = models.CharField(max_length=32, default='', blank=True)
    add_date   = models.DateTimeField(null=True)
    del_date   = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
