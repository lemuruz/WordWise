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

        # ตรวจสอบว่า response เป็น JSON และ status เป็น 200
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Word added successfully!")  # ตรวจสอบข้อความที่ได้จาก JSON

        # ตรวจสอบว่า `wordBank` มีคำ 'cookie' และประเภท 'noun'
        self.assertTrue(wordBank.objects.filter(word='cookie', word_type='noun', meaning="dessert that flavor sweet", translates="คุกกี้").exists())


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

        # ควรแสดงฟอร์มให้กรอกใหม่ หรือส่งกลับไปหน้าเดิม (ตรวจสอบสถานะ HTTP)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'menu/addword.html')  # แก้ไข

        # ตรวจสอบว่าไม่มีคำในฐานข้อมูล
        self.assertFalse(wordBank.objects.filter(word='', word_type='').exists())

    def test_add_same_word_with_different_meanings(self):
        # URL สำหรับฟอร์มเพิ่มคำ
        url = reverse('menu:add_word')

        # เพิ่มคำ 'tear' ในฐานข้อมูลที่มีความหมายเป็นคำใบ้ภาษาอังกฤษ 'to rip' และแปลว่า 'ฉีก'
        wordBank.objects.create(word='tear', word_type='verb', meaning='to rip', translates='ฉีก')

        # ส่งข้อมูลที่มีคำเดียวกันแต่ความหมายต่างกัน
        data = {
            'word': 'tear',  # คำเดียวกัน
            'word_type': 'noun',
            'word_mean': 'น้ำตา',  # ความหมายที่ต่างจากเดิม
            'word_clue': 'Something falls from your eye'
        }

        response = self.client.post(url, data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("message"), "Word added successfully!")

        # ตรวจสอบว่าในฐานข้อมูลมีทั้งสองคำ
        self.assertEqual(wordBank.objects.filter(word='tear').count(), 2)  
        self.assertEqual(wordBank.objects.filter(word='tear', translates='ฉีก').count(), 1)  
        self.assertEqual(wordBank.objects.filter(word='tear', meaning='to rip').count(), 1)  
        self.assertEqual(wordBank.objects.filter(word='tear', translates='น้ำตา').count(), 1)  

    def test_add_same_word_and_meaning(self):
        # URL สำหรับฟอร์มเพิ่มคำ
        url = reverse('menu:add_word')

        wordBank.objects.create(word='tear', word_type='verb', meaning='to rip', translates='ฉีก')

        data = {
            'word': 'tear',  # คำเดียวกัน
            'word_type': 'noun',
            'word_mean': 'ฉีก',  
            'word_clue': 'A tear falls from your eye'
        }

        response = self.client.post(url, data)

        # ตรวจสอบว่าได้รับ JsonResponse ว่า "This word and meaning already exist!" และสถานะ 400
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json().get("message"), "This word and meaning already exist!")

        # ตรวจสอบว่าในฐานข้อมูลยังมีแค่คำเดียวกับความหมายที่ถูกสร้างไว้แล้ว
        self.assertEqual(wordBank.objects.filter(word='tear').count(), 1)  # คำ 'tear' ไม่เพิ่มซ้ำ
        self.assertEqual(wordBank.objects.filter(word='tear', translates='ฉีก').count(), 1)  
        self.assertEqual(wordBank.objects.filter(word='tear', word_type='noun').count(), 0)  