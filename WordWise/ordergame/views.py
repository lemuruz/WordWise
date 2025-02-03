from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    return HttpResponse("ordergame")

def game(request):
    return render(request, 'ordergame/game.html')