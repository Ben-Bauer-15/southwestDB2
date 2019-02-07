from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .parser import *
from .models import *
from datetime import datetime
import threading
import urllib
import time


def index(req):
    return HttpResponse('Hello world!')


@csrf_exempt
def test(req):
    if req.method == "POST":
        return HttpResponse("Success")

    else:
        return HttpResponse("error")


@csrf_exempt
def startFareSearch(req):
    if req.method == 'POST':
        parser = MyParser()
        parser.findWannaGetAway(req.POST['siteData'])

        if parser.averagePrice == "Error" or parser.lowestPrice == "Error":
            return HttpResponse("Failure")
        
        else:
            search = FareSearch.objects.create(
                userEmail = req.POST['userEmail'],
                userPhone = req.POST['userPhone'],
                originAirport = req.POST['originAirport'],
                destinationAirport = req.POST['destinationAirport'],
                departureDate = req.POST['departingDate'],
                returnDate = req.POST['returningDate'],
                lowestPrice = parser.lowestPrice
            )

            AveragePrice.objects.create(
                search = search,
                price = parser.averagePrice
            )

            LowestPrice.objects.create(
                search = search,
                price = parser.lowestPrice
            )

            search.save()

            return HttpResponse("Created new search!")


@csrf_exempt
def validateUserContact(req):
    if req.method == 'POST':
        errors = FareSearch.objects.emailPhoneVal(req.POST)
        if errors:
            return HttpResponse("Form error")

        else:
            return HttpResponse("Success")
    else:
        return HttpResponse("Error")


@csrf_exempt
def updateFareSearch(req):
    if req.method == 'POST':
        parser = MyParser()
        parser.findWannaGetAway(req.POST['siteData'])
        
        if parser.averagePrice == "Error" or parser.lowestPrice == "Error":
            return HttpResponse("Failure")
        
        else:
            search = FareSearch.objects.get(id = req.POST['id'])
            search.updatedAt = datetime.now()

            AveragePrice.objects.create(
                search = search,
                price = parser.averagePrice
            )

            if parser.lowestPrice < search.lowestPrice:
                search.lowestPrice = parser.lowestPrice
                sendLowPriceText(search)

            search.save()

            return HttpResponse("Updated search query!")

    else:
        return HttpResponse("Error")



def recheckFares(threadName, id):
    SECONDS = 60
    MINUTES = 60
    HOURS = 24
    while True:
        searches = FareSearch.objects.all()
        for search in searches:
            postData = {'originAirport' : search.originAirport,
                        'destinationAirport' : search.destinationAirport,
                        'departingDate' : search.departureDate,
                        'returningDate' : search.returnDate,
                        'id' : search.id}

                        
            encoded = bytes( urllib.parse.urlencode(postData).encode() )
            result = urllib.request.urlopen('http://127.0.0.1:4000/recheckFares', encoded)

        
        print("Sleeping for ", SECONDS * MINUTES * HOURS, " seconds")
        time.sleep(SECONDS * MINUTES * HOURS)
    

threading._start_new_thread(recheckFares, ("New thread", 1))


def sendLowPriceText(search):
    postData = {'userPhone' : search.userPhone,
                'userEmail' : search.userEmail,
                'originAirport' : search.originAirport,
                'destinationAirport' : search.destinationAirport,
                'departingDate' : search.departureDate,
                'returningDate' : search.returnDate}

    encoded = bytes( urllib.parse.urlencode(postData).encode() )
    result = urllib.request.urlopen('http://127.0.0.1:4000/sendLowPriceText', encoded)
    print(result.read())