from django.test import TestCase
from django.urls import reverse

class MyViewTestCase(TestCase):
    def test_my_view(self):
        url = reverse('')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<h1>Hello, world!</h1>')
