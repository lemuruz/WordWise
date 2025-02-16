from django.shortcuts import render,redirect
from django.http import JsonResponse
from wordbank.models import wordBank


def index(request):
    return render(request,"menu/index.html")

def add_word(request):
    if request.method == "POST":
        word_text = request.POST.get("word", "").strip()  # ดึงค่าที่พิมพ์
        word_class = request.POST.get("word_type").strip()
        if word_text and word_class:  # ถ้าไม่ใช่ค่าว่าง
            wordBank.objects.get_or_create(word=word_text,word_type = word_class)  # เพิ่มคำลงฐานข้อมูล
            return redirect("menu:index")  # กลับไปหน้าเมนูหลังจากเพิ่มเสร็จ

    return render(request, "menu/addword.html")  # แสดงฟอร์ม

