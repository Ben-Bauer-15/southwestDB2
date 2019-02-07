from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\d{3}[-]\d{3}[-]\d{4}$')

class FareSearchManager(models.Manager):
    def emailPhoneVal(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['userEmail']):
            errors['email'] = 'Not a valid email'

        if not PHONE_REGEX.match(postData['userPhone']):
            errors['phone'] = 'Not a valid phone number'

        return errors


class FareSearch(models.Model):
    userEmail = models.CharField(max_length = 255)
    userPhone = models.CharField(max_length = 255)
    originAirport = models.CharField(max_length = 5)
    destinationAirport = models.CharField(max_length = 5)
    departureDate = models.CharField(max_length = 20)
    returnDate = models.CharField(max_length = 20)
    lowestPrice = models.FloatField()
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)
    objects = FareSearchManager()


class AveragePrice(models.Model):
    search = models.ForeignKey(FareSearch, related_name = 'averagePrices', on_delete = models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    price = models.FloatField()

class LowestPrice(models.Model):
    search = models.ForeignKey(FareSearch, related_name = 'lowestPrices', on_delete = models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    price = models.FloatField()
