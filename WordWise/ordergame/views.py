from django.shortcuts import render
from django.http import HttpResponse
from .models import sentences
# Create your views here.

def index(request):
    return HttpResponse("ordergame")

def game(request):
    random_sentence = sentences.objects.order_by('?').first().sentence
    return render(request, 'ordergame/game.html', {'the_sentence': random_sentence})