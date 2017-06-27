from __future__ import unicode_literals

from django.db import models
from django.contrib import admin

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=10)
    introduction = models.TextField()
    area = models.CharField(max_length=15)
    party_number = models.IntegerField(default=1)
    
    
    def __str__(self):
       return self.name

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
    # user_birth_month = models.IntegerField()
    # user_birth_day = models.IntegerField()
    # user_birth_year = models.IntegerField()
    def __str__(self):
       return self.username    
    
admin.site.register(User)


class Choice (models.Model):
	poll = models.ForeignKey(Poll)
	candidate = models.ForeignKey(Candidate)
	votes = models.IntegerField(default=0)
	
class Product (models.Model):
    name= models.CharField(max_length=10)
    introuduction= models.TextField()
    seller= models.ForeignKey(User)
    price = models.IntegerField()
    
class Wallet (models.Model):
    owner = models.ForeignKey(User)
    balance = models.IntegerField()
    
