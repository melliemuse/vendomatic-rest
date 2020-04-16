from django.db import models
from .customer import Customer
from .beverage import Beverage
from .payment import Payment

class Transaction(models.Model):
    customerId = models.ForeignKey(Customer, on_delete=models.CASCADE)  
    beverageId = models.ForeignKey(Beverage, on_delete=models.CASCADE)
    paymentId = models.ForeignKey(Payment, on_delete=models.CASCADE)
    completed = models.BooleanField