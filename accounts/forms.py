from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User, Group


class UserForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.CheckboxSelectMultiple(), required=False, help_text='Choose what type of polls you like.')

    class Meta:
        model = User
        fields = ['groups']


