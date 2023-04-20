from django.test import TestCase
from django.urls import reverse
from .models import RegularUser
from django.test import Client
# Create your tests here.


class MyViewTestCase(TestCase):
    def test_signup(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        url = reverse('login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class CreateUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('signup')
        self.user_data = {'username': 'testuser', 'email': 'testuser@example.com', 'password': 'password'}

    # def test_create_user(self):
    #     response = self.client.post(self.url, self.user_data)
    #     print(self.user_data)
    #     self.assertEqual(response.status_code, 200)
    #     count =RegularUser.objects.count()
    #     self.assertNotEqual(count, 0 , "User was created")
    #     self.assertTrue(RegularUser.objects.filter(username='testuser').exists())
