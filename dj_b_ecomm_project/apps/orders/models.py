# orders/models.py
from django.db import models
from django.conf import settings 
from apps.shop.models import Product
from django.utils.translation import gettext_lazy as _

class Order(models.Model):
    STATUS_CHOICES = (('pending', _("Pending")),
                      ('delivered', _("Delivered")),
                      ('cancelled', _("Cancelled"))
                      )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def __str__(self):
        username = self.user.username if self.user else "Unknown User"
        return f"Order - {username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def get_total(self):
        return self.price * self.quantity

