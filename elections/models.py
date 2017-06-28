from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.


class Poll (models.Model):
	start_date = models.DateTimeField()
	end_date = models.DateTimeField()
	area = models.CharField(max_length=15)

class User(models.Model):
    username = models.CharField(max_length=128,primary_key=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=255)
    authority = models.IntegerField(default=1)
    balance = models.IntegerField(default = 1000)
    # user_birth_month = models.IntegerField()
    # user_birth_day = models.IntegerField()
    # user_birth_year = models.IntegerField()
    def __str__(self):
       return self.username    
    
admin.site.register(User)


class Product(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField(null = True)
    area = models.CharField(max_length=15)
    price = models.IntegerField(default=100)
  # seller = models.ForeignKey(User)
    
    def __str__(self):
      return self.name


class Purchase (models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    #buyer = models.ForeignKey(User, on_delete = models.CASCADE)
    time = models.DateTimeField()

class Choice (models.Model):
	poll = models.ForeignKey(Poll)
	product = models.ForeignKey(Product)
	votes = models.IntegerField(default=0)
	

    

    
