from django.shortcuts import render,get_object_or_404,redirect
from django.urls import reverse
from .models import flashCardDeck,wordBank
import json,random
from django.http import JsonResponse
from user.models import Account,flashcardUserScore
from django.db.models import Avg, Count
from django.db.models.functions import Random
from django.db.models import Q
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
    deck_temp = get_object_or_404(flashCardDeck, id=deck_id)

    word_count = deck_temp.words.count()

    if word_count > 20:
        words_queryset = getflashcardselection(request, deck_id)  
    else:
        words_queryset = deck_temp.words.all()

    a_words = [{"word": e.word, "translates" : e.translates, "word_type" : e.word_type} for e in words_queryset]

    # print('>used>',len(words_queryset),words_queryset)
    #words = list(words_queryset.values('word', 'translates', 'word_type')) #list of dict type
    # print('uselist',len(words),words)
    return render(request,"flashcard/flashcardplayv2.html", {'deckname': deck_temp.name,
                                                           'flashcardwords': a_words})

def getflashcardselection(request,deck_id):
    username = request.session.get("username")
    user = Account.objects.get(username = username)
    deck = get_object_or_404(flashCardDeck, id=deck_id)
    all_words = deck.words.all()
    # print('allw',all_words)
    low_score_word = flashcardUserScore.objects.filter(account=user).order_by("score")[:7]

    low_score_word_texts = []
    for entry in low_score_word:
        low_score_word_texts.extend(entry.words.values_list("word", flat=True))  # Extract actual word texts

    low_score_words = wordBank.objects.filter(word__in=low_score_word_texts)

    used_words = flashcardUserScore.objects.filter(account=user).values_list("words", flat=True)
    new_words = list(all_words.exclude(id__in=used_words))[:7]
    
    remaining_slots = 20 - (len(new_words) + len(low_score_words))
    available_words = list(all_words.exclude(id__in=[w.id for w in new_words + list(low_score_words)]))
    random_words = random.sample(available_words, min(remaining_slots, len(available_words)))

    selected_words = list(new_words) + list(low_score_words) + list(random_words)
    random.shuffle(selected_words)

    # return  words_queryset[:20] 

    return selected_words[:20]




def flashcardend(request):
    return render(request,"flashcard/flashcardend.html")

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