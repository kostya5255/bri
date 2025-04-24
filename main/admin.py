from django.contrib import admin
from .models import Order, Product
import json

admin.site.register(Product)
admin.site.register(Order)
