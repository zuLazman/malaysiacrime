from django import forms
from django.utils.translation import ugettext as _

from models import Crime


class CrimeCreateForm(forms.ModelForm):
    """
    Form for entering crime information.
    """
    lat       = forms.FloatField(widget=forms.HiddenInput())
    lng       = forms.FloatField(widget=forms.HiddenInput())
    zoom      = forms.IntegerField(widget=forms.HiddenInput())
    password  = forms.CharField(max_length=20, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def clean_password2(self):
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        if password and (password != password2):
            raise forms.ValidationError(_("The passwords do not match."))
        return password2

    class Meta(object):
        model = Crime
        exclude = ['created_at', 'updated_at']

class CrimeUpdateForm(forms.ModelForm):
    """
    Form for entering crime information.
    """
    lat      = forms.FloatField(widget=forms.HiddenInput())
    lng      = forms.FloatField(widget=forms.HiddenInput())
    zoom     = forms.IntegerField(widget=forms.HiddenInput())
    password = forms.CharField(max_length=20, widget=forms.PasswordInput())

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password != self.instance.password:
            raise forms.ValidationError(_('The password is incorrect.'))
        return password

    class Meta(object):
        model = Crime
        exclude = ['created_at', 'updated_at']
