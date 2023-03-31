from django.db import models
#from accounts.models import User

# Create your models here.
class Aircraft(models.Model):
    id = models.BigAutoField(primary_key=True)
    currentSpeed = models.IntegerField()
    model = models.CharField(max_length = 50)
    fuelCapacity = models.IntegerField()
    timeForInspection = models.DateField()
    description = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='aircrafts/', blank=True, null=True)
    availability = models.BooleanField()

    #users = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
