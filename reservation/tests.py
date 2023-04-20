from django.test import TestCase
from django.urls import reverse
from .models import Aircraft

class MyViewTestCase(TestCase):
    def test_my_view(self):
        url = reverse('my_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


class MyPlaneTests(TestCase):
    def setUp(self):
        Aircraft.objects.create(id="1", currentSpeed="10" ,model ="Cesna" , fuelCapacity=100 , timeForInspection="2023-04-26" , description="Nice test" , image="aircrafts/goat.jpg", availability=True)
        Aircraft.objects.create(id="2", currentSpeed="10" ,model ="Cesna" , fuelCapacity=90 , timeForInspection="2023-04-25" , description="Nice test 2" , image="aircrafts/goat.jpg", availability=True)
    def test_PlaneCreation(self):
        count =Aircraft.objects.count()
        self.assertNotEqual(count, 0)