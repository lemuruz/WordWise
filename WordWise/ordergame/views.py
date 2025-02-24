from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import sentences, Account, orderUserScore
from random import random, choice
from django.db.models import F
import json
# Create your views here.

def get_random_sentence(master):
    user = Account.objects.filter(username=master).first()
    if random() < 0.2 and user:
        try:
            sen = list(orderUserScore.objects.filter(user=user).order_by(F('score').desc())[:5])
            return choice(sen).sentence.sentence
        except IndexError:
            pass
    ret_sent = sentences.objects.order_by('?').first()
    if ret_sent:
        return ret_sent.sentence
    else:
        return("I love ordergame.")

def game(request):
    try:
        master = request.session.get("username")
    except:
        master = ""
    random_sentence = get_random_sentence(master)
    addscoreurl = reverse("ordergame:addscore")
    return render(request, 'ordergame/game.html', {'the_sentence': random_sentence, 'add_sc_url': addscoreurl})

def test(request):
    return render(request, 'ordergame/game.html', {'the_sentence': 'I play violin.'})

def add_sentence(request):
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        sentence = request.POST.get('data')
        sentences.objects.create(sentence=sentence)
        return JsonResponse({"success": True})
    return render(request, 'ordergame/add_sentence.html')

def add_score(request):
    if request.method == 'POST':
        score = json.loads(request.body).get('gamescore')
        sentence = sentences.objects.get(sentence=json.loads(request.body).get('sentence'))
        username = request.session.get("username")
        account = Account.objects.get(username=username)
        scoreboard = orderUserScore.objects.filter(user=account, sentence=sentence).first()
        if scoreboard:
            scoreboard.score = ((scoreboard.score*scoreboard.times) + score) / (scoreboard.times + 1)
            scoreboard.times += 1
            scoreboard.save()
        else:
            scoreboard = orderUserScore.objects.create(user=account, sentence=sentence, score=score, times=1)
        return JsonResponse({"success": True})