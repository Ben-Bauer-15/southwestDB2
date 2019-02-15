from __future__ import unicode_literals
from django.db import models
import re
import urllib
import time as _t


SECONDS = 60
MINUTES = 60
HOURS = 24


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'^\d{3}[-]\d{3}[-]\d{4}$')

class FareSearchManager(models.Manager):
    def emailPhoneVal(self, postData):
        errors = {}
        if not EMAIL_REGEX.match(postData['userEmail']):
            errors['email'] = 'Not a valid email'

        if not PHONE_REGEX.match(postData['userPhone']):
            errors['phone'] = 'Not a valid phone number'


        user = FareSearch.objects.filter(userPhone = postData['userPhone'])
        return (user, errors)
    
    def recheckFares():
    
        while True:
            searches = FareSearch.objects.all()
            for search in searches:
                postData = {'originAirport' : search.originAirport,
                            'destinationAirport' : search.destinationAirport,
                            'departingDate' : search.departureDate,
                            'returningDate' : search.returnDate,
                            'id' : search.id}

                print("post data is ", postData)
                encoded = bytes( urllib.parse.urlencode(postData).encode() )

                try:
                    result = urllib.request.urlopen('http://southwest.ben-bauer.net/recheckFares', encoded)
                
                except:
                    print('Connection refused')

                
            print("Sleeping for ", 60, " seconds")
            print('testing!! :)')
            _t.sleep(60)


            


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


class Trip(models.Model):
    originAirport = models.CharField(max_length = 5)
    destinationAirport = models.CharField(max_length = 5)
    tripDate = models.DateTimeField()
    numFlights = models.IntegerField(default = 0)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)


class Flight(models.Model):
    departTime = models.CharField(max_length = 50)
    arriveTime = models.CharField(max_length = 50)
    duration = models.CharField(max_length = 50)
    businessFare = models.FloatField()
    anytimeFare = models.FloatField()
    wannaGetAwayFare = models.FloatField()
    numStops = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(auto_now_add = True)
    trip = models.ForeignKey(Trip, related_name = 'flights', on_delete = models.CASCADE)
