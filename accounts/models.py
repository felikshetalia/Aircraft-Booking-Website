from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)
    email = models.EmailField(max_length=80)
    passwd = models.CharField()

    class Meta:
        abstract = True

    def __str__(self):
        return self.name + self.surname

class RegularUser(User, AbstractUser):
    user_field = models.CharField(max_length=50)

class Employee(User, AbstractUser):
    id = models.IntegerField(null=False, unique=True)
    certificate = models.ImageField(upload_to='certificates/')
    salary = models.IntegerField()

    class Meta:
        abstract = True


class Admin(Employee, AbstractUser):
    admin_field = models.CharField(max_length=50)


class Engineer(Employee, AbstractUser):
    inz_field = models.CharField(max_length=50)
