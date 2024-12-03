from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClientDetails(models.Model):
    id=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    phone=models.IntegerField(unique=True)
    photo=models.ImageField(upload_to='Customers')
    address=models.TextField(max_length=100)
    def __str__(self):
        return self.first_name

class userprofile(models.Model):
    name=models.CharField(max_length=40)
    email=models.EmailField()
    phone=models.IntegerField()
    address=models.TextField()
    profilepicture=models.ImageField(upload_to='Customers',null=True,blank=True)
    def __str__(self):
        return self.name