from django.test import TestCase
from django.urls import reverse
from wordbank.models import wordBank

class WordBankTests(TestCase):

    def test_add_word_valid_data(self):
        # URL สำหรับฟอร์มเพิ่มคำ
        url = reverse('menu:add_word')

        # ข้อมูลที่เราต้องการส่งไปยังฟอร์ม
        data = {
            'word': 'cookie',
            'word_type': 'noun',
            'word_mean': "คุกกี้",
            'word_clue': 'dessert that flavor sweet'
        }

        # ส่งคำร้อง POST ไปยังฟอร์ม
        response = self.client.post(url, data)

        # ตรวจสอบว่า redirect ไปที่หน้า menu
        self.assertRedirects(response, reverse('menu:index'))  

        # ตรวจสอบว่า `wordBank` มีคำ 'example' และประเภท 'noun'
        self.assertTrue(wordBank.objects.filter(word='cookie', word_type='noun', meaning = "dessert that flavor sweet", translates = "คุกกี้").exists())

    def test_add_word_empty_data(self):
        # URL สำหรับฟอร์มเพิ่มคำ
        url = reverse('menu:add_word')

        # ข้อมูลที่ไม่กรอกอะไรเลย
        data = {
            'word': '',
            'word_type': '',
            'word_mean': "",
            'word_clue': ''
            
        }

        # ส่งคำร้อง POST ไปยังฟอร์ม
        response = self.client.post(url, data)

        # ควรแสดงฟอร์มให้กรอกใหม่หรือส่งกลับไปหน้าเดิม (ตรวจสอบสถานะ HTTP)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/addword.html')  # แก้ไข

        # ตรวจสอบว่าไม่มีคำในฐานข้อมูล
        self.assertFalse(wordBank.objects.filter(word='', word_type='').exists())


<<<<<<< HEAD
=======
        # ข้อมูลที่กรอกคำแต่ไม่กรอกประเภทคำ
        data = {
            'word': 'example',
            'word_type': 'dsjkfj'
        }

        # ส่งคำร้อง POST ไปยังฟอร์ม
        response = self.client.post(url, data)

        # ควรแสดงฟอร์มให้กรอกใหม่หรือส่งกลับไปหน้าเดิม
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/addword.html')  # แก้ไข

        # ตรวจสอบว่าไม่มีคำในฐานข้อมูล
        self.assertFalse(wordBank.objects.filter(word='example', word_type='').exists())
>>>>>>> aecaeb1a8fba476464d95972edb1f18ace5255dd

    def test_add_word_duplicate(self):
        # URL สำหรับฟอร์มเพิ่มคำ
        url = reverse('menu:add_word')

        # เพิ่มคำเดียวกันในฐานข้อมูลก่อน
        wordBank.objects.create(word='cookie', word_type='noun',meaning = 'dessert that flavor sweet', translates = "คุกกี้")

        # ส่งคำร้อง POST ไปยังฟอร์มด้วยข้อมูลซ้ำ
        data = {
            'word': 'cookie',
            'word_type': 'noun',
            'word_mean': "คุกกี้",
            'word_clue': 'dessert that flavor sweet'
        }

        response = self.client.post(url, data)

        # ควร redirect ไปหน้า menu และไม่เพิ่มข้อมูลใหม่
        self.assertRedirects(response, reverse('menu:index'))  # แก้ไข
        
        # ตรวจสอบว่าในฐานข้อมูลมีแค่คำเดียว ไม่เพิ่มคำซ้ำ
        self.assertEqual(wordBank.objects.filter(word='cookie', word_type='noun').count(), 1)
