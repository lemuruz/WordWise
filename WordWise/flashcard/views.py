from django.shortcuts import render,get_object_or_404,redirect
from .models import flashCardDeck
import random
# from django.http import HttpResponse
# Create your views here.

def index(request):
    deck = flashCardDeck.objects.all()
    return render(request,"flashcard/flashcardmenu.html",{'flashcarddeck':deck})

def flashcardplay(request, deck_id):
    deck = get_object_or_404(flashCardDeck, id=deck_id)
    words = list(deck.words.all().values('word', 'translates', 'word_type'))
    return render(request,"flashcard/flashcardplayv2.html", {'deckname': deck.name,
                                                           'flashcardwords': words})

def flashcardend(request):
    return render(request,"flashcard/flashcardend.html")

# def flashcardplay(request, deck_id):
#     request.session["deck_id"] = deck_id
#     deck = get_object_or_404(flashCardDeck, id=deck_id)
#     words = deck.words.all()

#     if "flashcard_index" not in request.session:
#         request.session["flashcard_index"] = 0  # Start from first word
#         request.session["flashcard_order"] = random.sample(range(len(words)), len(words))  # Shuffle words

#     index = request.session["flashcard_index"]
#     word_order = request.session["flashcard_order"]

#     # If all words are finished, reset session or redirect
#     if index >= len(words):
#         del request.session["flashcard_index"]  # Reset index
#         del request.session["flashcard_order"]  # Reset order
#         return redirect('flashcard:index')  # Redirect to a completion page

#     current_word = words[word_order[index]]  # Get the current word

#     return render(request, "flashcard/flashcardplay.html", {'deckname':deck,
#                                                             'flashcardwords': current_word})

# def next_word(request):
#     request.session["flashcard_index"] += 1
#     # If your flashcardplay view requires a deck_id, you might need to pass that too:
#     deck_id = request.session.get("deck_id")  # Make sure to store this in the session when starting
#     return redirect('flashcard:flashcardplay', deck_id=deck_id)
