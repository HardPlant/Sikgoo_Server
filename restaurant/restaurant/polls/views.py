from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice
from django.shortcuts import get_object_or_404
from .models import User

import json

import requests

def index(request):
    q = Question.objects.get(pk=1)
    dicts = dict({
        'question_text': q.question_text,
        'pub_date' : str(q.pub_date)
    })
    return HttpResponse(json.dumps(dicts))

def register(request, user_id):
    try:
        token = request.post['token']
        User(token=token).save()
    except KeyError:
        return HttpResponse(status=404)

def send_notification(request):
    sess = requests.Session()
    data = dict({
        'registration_ids' : ['fYCEXoL3ah8:APA91bFk5M3ehQYs7TtHm9k-ggwLQzEezZzzZ1YluZq8LhefMw_w3LW0D8o46JEPcqirdIby5n5L1FHcP6mpk6xrvg6dQHYz1pjeDS4XsdL0rhabnX84s0INx9RCXL95LUgW63ewhILm'],
        'data': dict({'title':'hello',
                      'body':'Hello Console'})
    })
    JSON = json.dumps(data)

    req = requests.Request('POST', 'https://fcm.googleapis.com/fcm/send',json=JSON)
    prep = req.prepare()
    prep.headers['Authorization'] = 'key =' + 'AAAAxB9zt8Q:APA91bHT6z60Edfx_lKh-v2Jf-yeRNB9hjnaG42n1cpJ-aitrXHUD8KPDjxUZK8fvmuxqyfxp0NhviphjiFOOaGx_N8xtAObezaKzhkCOwdFehGFzY_lyege23Rl5WrpsuLieJVLP18i'

    sess.send(prep)