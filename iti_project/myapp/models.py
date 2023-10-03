from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    is_admin = models.BooleanField(default=False)

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, null=False)
    description = models.CharField(max_length=150, null=False)
    is_borrowed = models.BooleanField(default=False)
    borrowed_by_id = models.ForeignKey(User,null=True, on_delete=models.SET_NULL)
    returnTime = models.DateTimeField(null=True)
    photoName = models.CharField(max_length=50, default="1.jpg")
