from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _


class UserForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(label=_('Groups'), queryset=Group.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(), required=False, help_text=_('Choose what type of polls you like.'))

    class Meta:
        model = User
        fields = ['groups']


