from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.

class User(models.Model):
    id = models.CharField(max_length=10, null=False, unique=True, primary_key=True)
    name = models.CharField(max_length = 50)
    surname = models.CharField(max_length = 50)
    email = models.EmailField(max_length=80, unique=True)
    passwd = models.CharField(max_length=30)

    class Meta:
        # abstract = True
        pass

    def __str__(self):
        return self.name + self.surname

class RegularUser(User):
    user_field = models.CharField(max_length=50)
    db_table = 'member'

class Employee(User):
    #id = models.IntegerField(null=False, unique=True)
    certificate = models.ImageField(upload_to='certificates/')
    salary = models.IntegerField()
    db_table = 'employee'


class Admin(Employee):
    is_superuser = models.BooleanField()
    admin_field = models.CharField(max_length=50)
    class Meta:
        db_table = 'admin'


class Engineer(Employee, AbstractUser):
    department = models.CharField(max_length=50)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='engineers',
        blank=True,
        help_text='The groups this engineer belongs to. A engineer will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='engineers',
        blank=True,
        help_text='Specific permissions for this engineer.',
        verbose_name='user permissions',
    )
    class Meta:
        db_table = 'engineer'
