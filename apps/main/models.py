from __future__ import unicode_literals
from django.db import models

class FareSearch(models.Model):
    userEmail = models.CharField(max_length = 255)
    userPhone = models.CharField(max_length = 255)
    originAirport = models.CharField(max_length = 5)
    destinationAirport = models.CharField(max_length = 5)
    departureDate = models.CharField(max_length = 20)
    returnDate = models.CharField(max_length = 20)
    lowestPrice = models.IntegerField(default = 0)
    averagePrice = models.IntegerField(default = 0)