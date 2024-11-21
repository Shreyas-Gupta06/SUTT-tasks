
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse

# Create your views here.
def index(request):
    questionList = Question.objects.order_by("-pubDate")[:5]
    template = loader.get_template("Polls/index.html")
    context = {
        "questionList" : questionList,
    }
    return HttpResponse(template.render(context, request))

def questionDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    # try:
    #     question = Question.objects.get(pk=question_id)
    # except Question.DoesNotExist:
    #     raise Http404("Question does not exist")
    return render(request, "Polls/detail.html", {"question":question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "Polls/results.html", {"question" : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selectedChoice = question.choice_set.get(pk=request.POST["choice"])
    except(KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question":question, "errorMessage":"You didn't select a choice.",})
    else:
        selectedChoice.votes = F("votes") + 1
        selectedChoice.save()
        return HttpResponseRedirect(reverse("Polls:results", args=(question.id,)))