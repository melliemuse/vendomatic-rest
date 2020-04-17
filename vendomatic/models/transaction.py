from django.db import models
from .customer import Customer
from .beverage import Beverage

class Transaction(models.Model): 
    beverageId = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    coin = models.IntegerField()