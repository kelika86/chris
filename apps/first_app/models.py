from django.db import models
from django.db.models import Sum, Aggregate, FloatField, F, ExpressionWrapper

class User(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.CharField(max_length=100)
    password=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Ticket(models.Model):
    venue=models.CharField(max_length=100)
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(default=25.00, max_digits=5, decimal_places=2, null=True, blank=True)
    loop=models.CharField(max_length=100)
    purchaser = models.ForeignKey(User, related_name="purchases", on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

class Order(models.Model):
    full_name=models.CharField(max_length=100)
    cc_number=models.PositiveIntegerField()
    exp_date=models.PositiveIntegerField()
    cvc=models.PositiveIntegerField()
    buyers=models.ManyToManyField(Ticket, related_name="bought_tickets")
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
   
