from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, JsonResponse
from .models import sentences, userScore, Account
import json
# Create your views here.

def game(request):
    random_sentence = sentences.objects.order_by('?').first().sentence
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
        username = request.session.get("username")
        account = Account.objects.get(username=username)
        scoreboard = userScore.objects.filter(user=account).first()
        if scoreboard:
            scoreboard.score = ((scoreboard.score*scoreboard.times) + score) / (scoreboard.times + 1)
            scoreboard.times += 1
            scoreboard.save()
        else:
            scoreboard = userScore.objects.create(user=account, score=score, times=1)
        return JsonResponse({"success": True})