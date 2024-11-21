from django.contrib import admin
from .models import Question, Choice
# Register your models here.
# admin.site.register(Question)
admin.site.register(Choice)

class ChoiceInLine(admin.StackedInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields":["questionText"]}),
        ("Date Information", {"fields": ["pubDate"], "classes":["collapse"]})
    ]
    inlines = [ChoiceInLine]



admin.site.register(Question, QuestionAdmin)