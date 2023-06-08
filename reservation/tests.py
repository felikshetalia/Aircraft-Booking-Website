from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase, Client , RequestFactory
from django.contrib.auth.models import User
from datetime import datetime, timedelta

from django.utils.dateparse import parse_datetime

from .models import Aircraft, Booking
from accounts.forms import UserSignUpForm
from unittest.mock import patch
from .views import connect, getToken



class MyViewTestCase(TestCase):
    def test_my_view(self):
        url = reverse('my_view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    
def test_login(self):
        url = reverse('engineer')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)


def test_login(self):
        url = reverse('Planes')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)



class MyPlaneTests(TestCase):
    def setUp(self):
        Aircraft.objects.create(id="1", currentSpeed="10", model ="Cesna", fuelCapacity=100, timeForInspection="2023-04-26", description="Nice test", image="media/pics/oip.jpg", availability=True)
        Aircraft.objects.create(id="2", currentSpeed="10", model ="Cesna", fuelCapacity=90, timeForInspection="2023-04-25", description="Nice test 2", image="media/pics/oip (1).jpg", availability=True)
    def test_PlaneCreation(self):
        count =Aircraft.objects.count()
        self.assertNotEqual(count, 0)


class BookAircraftViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.aircraft = Aircraft.objects.create(id="3", currentSpeed="10", model ="Cesna", fuelCapacity=100, timeForInspection="2023-04-26", description="Nice test", image="media/pics/oip.jpg", availability=True)
        form_data = {
            'username': 'testuser2',
            'password1': 'NotEasyPassword124^',
            'password2': 'NotEasyPassword124^',
            'email': 'testuser2@example.com',
        }
        form = UserSignUpForm(data=form_data)
        if not form.is_valid():
            print(form.errors)
      
        self.user = form.save()
        print(self.user.username)
        self.url = reverse('book_aircraft')

    def test_anonymous_user_redirected(self):
        """Test that an anonymous user is redirected to the login page."""
        response = self.client.get(self.url)
        self.assertRedirects(response, f'/accounts/login/?next={self.url}')

    def test_logged_in_user_can_book_aircraft(self):
        """Test that a logged-in user can book an aircraft."""
        self.client.login(username='testuser2', password='NotEasyPassword124^')

        # Create a booking for the aircraft
        start_time = datetime.now() + timedelta(hours=1)
        end_time = start_time + timedelta(hours=2)
        response = self.client.post(self.url, {
            'aircraft_id': self.aircraft.id,
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
        })

        # Check that the booking was created
        booking = Booking.objects.first()
        print(booking)
        print("here here")
        self.assertEqual(booking.aircraft, self.aircraft)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.status, 'Pending')
        self.assertTrue(self.aircraft.availability)


    def test_missing_required_fields(self):
        """Test that an error is shown when required fields are missing."""
        self.client.login(username='testuser2', password='NotEasyPassword124^')
        response = self.client.post(self.url, {})
        self.assertContains(response, 'Missing required fields')

    # def test_invalid_datetime_format(self):
    #     """Test that an error is shown when an invalid datetime format is provided."""
    #     self.client.login(username='testuser2', password='NotEasyPassword124^')
    #     response = self.client.post(self.url, {
    #         'aircraft_id': self.aircraft.id,
    #         'start_time': 'invalid_datetime',
    #         'end_time': 'invalid_datetime',
    #     })
    #     self.assertContains(response, 'Invalid datetime format')

    def test_end_time_before_start_time(self):
        """Test that an error is shown when the end time is before the start time."""
        self.client.login(username='testuser2', password='NotEasyPassword124^')
        response = self.client.post(self.url, {
            'aircraft_id': self.aircraft.id,
            'start_time': '2023-05-09T12:00:00',
            'end_time': '2023-05-09T11:00:00',
        })
        self.assertContains(response, 'End time must be after start time')


    





####Integration 
#  NEEDS TO BE COMMENTS since to pass we need an instance of the other team server runnning on local host



# class ConnectTestCase(TestCase):
#     def setUp(self):
#         self.factory = RequestFactory()

#     @patch('requests.post')
#     def test_connect_returns_token(self, mock_post):
#         mock_post.return_value.status_code = 201
#         mock_post.return_value.json.return_value = {'access': 'test_token'}

#         request = self.factory.get('/connect/')
#         response = connect(request)

#         self.assertIn('token', response.content.decode())

#     @patch('requests.post')
#     def test_connect_returns_error(self, mock_post):
#         mock_post.return_value.status_code = 400
#         mock_post.return_value.json.return_value = {'error': 'Invalid credentials'}

#         request = self.factory.get('/connect/')
#         response = connect(request)

#         self.assertNotIn('token', response.content.decode())
=======

class BookAircraftViewTest(TestCase):
    def setUp(self):
        # Create a test user
        self.client = Client()
        form_data = {
            'username': 'testuser3',
            'password1': 'NotEasyPassword124^',
            'password2': 'NotEasyPassword124^',
            'email': 'testuser3@example.com',
        }
        form = UserSignUpForm(data=form_data)
        if not form.is_valid():
            print(form.errors)

        self.user = form.save()

        # Create some test aircrafts
        self.aircraft1 = Aircraft.objects.create(id="3", currentSpeed="10", model="Cesna1", fuelCapacity=100, timeForInspection="2023-04-26", description="Nice test", image="static/Aircrafts_img/AirbusA380.jpeg", availability=True)
        self.aircraft2 = Aircraft.objects.create(id="4", currentSpeed="10", model="Cesna2", fuelCapacity=200, timeForInspection="2023-05-26", description="Nice test", image="static/Aircrafts_img/Biplane.jpeg", availability=True)

    def test_book_aircraft_with_valid_data(self):
        # Log in the test user
        self.client.login(username='testuser3', password='NotEasyPassword124^')

        # Prepare the data for booking
        aircraft_id = self.aircraft1.id
        start_time_str = '2023-04-23 09:00:00'
        end_time_str = '2023-05-23 12:00:00'

        # Send a POST request to book the aircraft
        response = self.client.post(reverse('book_aircraft'), {
            'aircraft_id': aircraft_id,
            'start_time': start_time_str,
            'end_time': end_time_str,
        })

        # Assert that the booking is created in the database
        booking = Booking.objects.get(id=1)
        self.assertEqual(booking.aircraft, self.aircraft1)
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.status, 'Pending')

        # Assert that the aircraft availability is updated
        self.aircraft1.refresh_from_db()
        self.assertFalse(self.aircraft1.availability)

    def test_cancel_booking(self):
        # Create a booking for the user
        booking = Booking.objects.create(aircraft=self.aircraft1, user=self.user, start_time='2023-05-22T10:00:00Z',
                                         end_time='2023-05-22T12:00:00Z', status='Pending')

        # Login the user
        self.client = Client()
        self.client.login(username='testuser3', password='NotEasyPassword124^')

        # Send a POST request to cancel the booking
        response = self.client.post(reverse('cancel_booking', args=[booking.id]))

        # Assert that the booking is cancelled and the aircraft availability is set to True
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Cancelled')
        self.assertTrue(self.aircraft1.availability)

        # Assert that the user is redirected to the booking list page
        self.assertRedirects(response, reverse('booking_list'))

