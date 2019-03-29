from django.db import models
from django.db.models import Sum, Aggregate

class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    venue=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField(default=1)
    price=models.DecimalField(default=25.00, max_digits=10, decimal_places=2, null=True, blank=True)
    loop=models.CharField(max_length=100)
    purchaser = models.ForeignKey(User, related_name="purchases", on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    @property
    def total(self):
        q= self.price * self.quantity
        t= q *0.0725
        totalPrice= t + self.price
        return totalPrice
