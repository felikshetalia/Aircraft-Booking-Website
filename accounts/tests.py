from django.test import TestCase
from django.urls import reverse
# Create your tests here.


class MyViewTestCase(TestCase):
    def test_signup(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)