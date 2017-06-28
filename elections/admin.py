from django.contrib import admin

from .models import Product, Poll, Choice
# Register your models here.



admin.site.register(Product)
admin.site.register(Poll)
admin.site.register(Choice)
