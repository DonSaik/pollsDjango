from django.db import models
from django.contrib.auth.models import User, Group
from django.utils.translation import ugettext_lazy as _
# Create your models here.


class Question(models.Model):
    question_text = models.CharField(_("Question text"), max_length=200)
    created_at = models.DateTimeField('date_created_at', auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    groups = models.ManyToManyField(Group)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(_("Choice text"), max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

