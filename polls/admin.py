from django.contrib import admin

# Register your models here.
from .models import Question, Choice, Vote


class ChoiceInine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'groups', 'user']}),
    ]
    inlines = [ChoiceInine]
    list_display = ('id', 'question_text', 'created_at')
    search_fields = ['question_text']
    list_filter = ['created_at']


admin.site.register(Question, QuestionAdmin)
admin.site.register(Vote)
