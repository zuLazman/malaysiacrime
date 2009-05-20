from django import forms

from models import Moniton


class SubscribeForm(forms.ModelForm):
    """
    Form for subscribing to monitor.
    """
    class Meta(object):
        model = Moniton
        exclude = ['registered', 'add_uuid', 'del_uuid', 'add_date', 'del_date', 'created_at', 'updated_at']
