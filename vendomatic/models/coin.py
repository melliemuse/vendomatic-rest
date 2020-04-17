from django.db import models


class Coin(models.Model):
    coin = models.IntegerField()
