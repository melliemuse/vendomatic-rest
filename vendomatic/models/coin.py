from django.db import models

class Coin(models.Model):
    coinType = models.CharField(max_length=25)
    quantity = models.IntegerField()