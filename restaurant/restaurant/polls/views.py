from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
import json

def index(request):
    q = Question.objects.get(pk=1)
    dicts = dict({
        'question_text': q.question_text,
        'pub_date' : str(q.pub_date)
    })
    return HttpResponse(json.dumps(dicts))