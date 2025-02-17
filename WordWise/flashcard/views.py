from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import flashCardDeck,wordBank
import json
from django.http import JsonResponse
from user.models import Account,flashcardUserScore

def index(request):
    username = request.session.get("username")
    if not username:
        return redirect(reverse('user:login'))
    
    user = Account.objects.filter(username=username).first()

    if not user:
        return redirect(reverse('user:login'))
    
    deck = user.flashcard.all()
    return render(request,"flashcard/flashcardmenu.html",{'flashcarddeck':deck,
                                                            'user' : user})

def flashcardplay(request, deck_id):
    deck = get_object_or_404(flashCardDeck, id=deck_id)
    words = list(deck.words.all().values('word', 'translates', 'word_type'))
    return render(request,"flashcard/flashcardplayv2.html", {'deckname': deck.name,
                                                           'flashcardwords': words})

def flashcardend(request):
    score = request.GET.get('score',0)
    flashcard_length = request.GET.get('flashcardlength',0)
    return render(request,"flashcard/flashcardend.html",{
        'score' : score,
        'maxscore' : int(flashcard_length)*3,
    })

def createDeck(request):
    words = wordBank.objects.all().values("id", "word", "word_type")  # Fetch words
    username = request.session.get("username")
    if not username:
        return redirect(reverse('user:login'))
    
    user = Account.objects.filter(username=username).first()
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            deck_name = data.get("deck_name")
            words = data.get("words", [])

            if not deck_name:
                return JsonResponse({"error": "Deck name is required"}, status=400)
            
            deck, created = flashCardDeck.objects.get_or_create(name=deck_name)
            deck.words.set(wordBank.objects.filter(id__in=words))

            user.flashcard.add(deck)  
            
            return JsonResponse({"message": "Flashcard deck created successfully"}, status=201)
        
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)
    return render(request, "flashcard/flashcardcreate.html", {"words": list(words)})


def addUserScore(request):
    username = request.session.get("username")
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            word = data.get("word")
            score = data.get("score")
            temp = wordBank.objects.get(word=word["word"],word_type = word["word_type"])
            user = Account.objects.get(username = username)
            try:
                user_score = flashcardUserScore.objects.get(words=temp,account=user)
                user_score.score = ((user_score.score*user_score.answerCount) + score)/(user_score.answerCount + 1)
                user_score.answerCount = user_score.answerCount + 1
                user_score.save()
            except:
                user_score = flashcardUserScore.objects.create(score=score, answerCount=1)

                user_score.words.set([temp])
                user_score.account.set([user])

                
            return JsonResponse({"message": "add complete"}, status=201)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data"}, status=400)