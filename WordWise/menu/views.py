from django.shortcuts import render,redirect
from django.http import JsonResponse
from wordbank.models import wordBank


def index(request):
    return render(request,"menu/index.html")

def add_word(request):
    if request.method == "POST":
        word_text = request.POST.get("word", "").strip()
        word_class = request.POST.get("word_type", "").strip()
        word_mean = request.POST.get("word_mean", "").strip()
        word_clue = request.POST.get("word_clue", "").strip()

        if word_text and word_class and word_mean and word_clue:
            if wordBank.objects.filter(word=word_text, translates=word_mean).exists():
                return JsonResponse({"message": "This word and meaning already exist!"}, status=400)
            else:
                wordBank.objects.create(
                    word=word_text, word_type=word_class, meaning=word_clue, translates=word_mean
                )
                return JsonResponse({"message": "Word added successfully!"}, status=200)

    return render(request, "menu/addword.html")

