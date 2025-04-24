from django.db import models
import json


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)  #

    def __str__(self):
        return self.name


class Order(models.Model):
    name = models.CharField(max_length=100, default="Имя")
    phone = models.CharField(max_length=15, default="000000000")
    address = models.TextField(default="000000000")
    cart_data = models.TextField(
        default="empty"
    )  # <-- Stores cart content as JSON string
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default="0")
    created_at = models.DateTimeField(auto_now_add=True)

    def set_cart_data(self, cart_items):
        self.cart_data = json.dumps(cart_items)

    def get_cart_data(self):
        return json.loads(self.cart_data)

    def __str__(self):
        return f"Order #{self.id} by {self.name}"
