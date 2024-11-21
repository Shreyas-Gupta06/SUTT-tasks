import datetime

#django modules
from django.db import models
from django.utils import timezone

#models 
class Question(models.Model):
    questionText = models.CharField(max_length=200)
    pubDate = models.DateTimeField("date published")
    
    def __str__(self):
        return self.questionText
    def wasPublishedRecently(self):
        return self.pubDate >= timezone.now() - datetime.timedelta(days=1)
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choiceText = models.CharField(max_length=300)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choiceText
