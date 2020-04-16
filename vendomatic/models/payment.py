from django.db import models
from .coin import Coin

class Payment(models.Model):
    coinId = models.ForeignKey(Coin, on_delete=models.CASCADE)
    quantity = models.IntegerField()