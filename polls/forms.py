from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from django import forms
from polls.models import Question, Choice
from django.contrib.auth.models import Group


class PollForm(ModelForm):
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all(),
                                            widget=forms.CheckboxSelectMultiple())

    class Meta:
        model = Question
        fields = ['question_text', 'groups']
        widgets = {
            'question_text': forms.TextInput(
                attrs={
                    'class': 'form-control',
                }
            )
        }


ChoiceFormset = modelformset_factory(
    Choice,
    fields=('choice_text', ),
    min_num=2,
    extra=1,
    widgets={
        'choice_text': forms.TextInput(
            attrs={
                'class': 'form-control',
            }
        )
    }
)