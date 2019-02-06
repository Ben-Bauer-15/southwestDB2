from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .parser import *
from .models import *
from .schedule import scheduler
import threading
import time

def index(req):
    return HttpResponse('Hello world!')


@csrf_exempt
def test(req):
    if req.method == "POST":
        print(req.POST)
        return HttpResponse("Success")

    else:
        print("error")
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
                lowestPrice = parser.lowestPrice,
                averagePrice = parser.averagePrice
            )

            # print(search.averagePrice, search.lowestPrice)
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





def testThread(threadName, id):
    while True:
        print('testing a thread with name', threadName)
        print("id param is ", id)
        time.sleep(5)
    
threading._start_new_thread(testThread, ("New thread", 1))