from django.db import models

from accounts.models import User
#from accounts.models import User
# Create your models here.


class Aircraft(models.Model):
    id = models.BigAutoField(primary_key=True)
    currentSpeed = models.IntegerField()
    model = models.CharField(max_length=50)
    fuelCapacity = models.IntegerField()
    timeForInspection = models.DateField()
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='static/Aircrafts_img/', blank=True, null=True)
    availability = models.BooleanField()
    country = models.CharField(max_length=100,default='Unknown')


    #users = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
class Booking(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    ]
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')


class Review(models.Model):
    RATING_CHOICES = [(i, i) for i in range(1, 6)]
    aircraft = models.ForeignKey(Aircraft, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=1000)
    rating = models.IntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


