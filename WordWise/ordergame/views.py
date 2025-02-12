from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import sentences
# Create your views here.

def game(request):
    random_sentence = sentences.objects.order_by('?').first().sentence
    return render(request, 'ordergame/game.html', {'the_sentence': random_sentence})

def test(request):
    return render(request, 'ordergame/game.html', {'the_sentence': 'I play violin.'})

def add_sentence(request):
    if request.method == 'POST' and request.headers.get("X-Requested-With") == "XMLHttpRequest":
        sentence = request.POST.get('data')
        #sentences.objects.create(sentence=sentence)
        return JsonResponse({"success": True})
    return render(request, 'ordergame/add_sentence.html')