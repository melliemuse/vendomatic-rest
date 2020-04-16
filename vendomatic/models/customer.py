from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .coin import Coin

class Customer(models.Model):
    name = models.CharField(max_length=50)
    coinId = models.ForeignKey(Coin, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)