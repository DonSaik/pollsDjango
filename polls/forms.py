from django.forms import ModelForm, modelformset_factory, inlineformset_factory
from django import forms
from polls.models import Question, Choice


class PollForm(ModelForm):

    class Meta:
        model = Question
        fields = ['question_text']


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