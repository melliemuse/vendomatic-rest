from django.db import models


class Beverage(models.Model):
    beverageType = models.CharField(max_length=50)
    price = models.IntegerField()
    quantity = models.IntegerField()
    stock = models.IntegerField()


