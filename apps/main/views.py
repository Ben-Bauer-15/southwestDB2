from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .parser import *
from .models import *




def index(request):
    return HttpResponse('Hello world!')


@csrf_exempt
def test(request):
    if request.method == "POST":    
        print(request.POST)
        return HttpResponse("Success")

    else:
        print("error")
        return HttpResponse("error")


@csrf_exempt
def parserTest(request):
    if request.method == 'POST':
        print(request.POST)
        # print(request.POST['userPhone'])
        # parser = MyParser()

        # parser.feed(request.POST['data'])


        return HttpResponse("Success!")



@csrf_exempt
def startFareSearch(request):
    if request.method == 'POST':
        parser = MyParser()
        parser.findWannaGetAway(request.POST['siteData'])
        if parser.averagePrice == "Error" or parser.lowestPrice == "Error":
            return HttpResponse("Failure")
        
        else:
            errors = FareSearch.objects.emailPhoneVal(request.POST)
            if errors:
                return HttpResponse("Form error")
            else:
                search = FareSearch.objects.create(
                    userEmail = request.POST['userEmail'],
                    userPhone = request.POST['userPhone'],
                    originAirport = request.POST['originAirport'],
                    destinationAirport = request.POST['destinationAirport'],
                    departureDate = request.POST['departingDate'],
                    returnDate = request.POST['returningDate'],
                    lowestPrice = parser.lowestPrice,
                    averagePrice = parser.averagePrice
                )

                # print(search.averagePrice, search.lowestPrice)
                return HttpResponse("Created new search!")

    
