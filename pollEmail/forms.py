from django import forms
from django.utils.translation import ugettext_lazy as _


class EmailForm(forms.Form):
    address = forms.CharField(label=_('Address'), max_length=100)
    subject = forms.CharField(label=_('Subject'), max_length=100)
    message = forms.CharField(label=_('Message'), widget=forms.Textarea)
