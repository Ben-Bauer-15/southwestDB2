from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from .parser import *
from .models import *
from datetime import datetime
from threading import Thread
import urllib.request
import time as _t
from django.http import JsonResponse
from .searchGenerator import *
import json
from multiprocessing import Process



def index(req):
    return HttpResponse('Hello world! This is the landing page for the SWA API :)')

def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target = function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


def getAllSearches(req):
    searches = FareSearch.objects.all()

    myList = []

    for search in searches:
        myList.append({'userEmail' : search.userEmail,
                        'userPhone' : search.userPhone,
                        'originAirport' : search.originAirport,
                        'destinationAirport' : search.destinationAirport,
                        'depart' : search.departureDate,
                        'return' : search.returnDate,
                        'lowestPrice' : search.lowestPrice })

    return JsonResponse(myList, safe=False)

@csrf_exempt
def test(req):
    if req.method == "POST":
        return HttpResponse("Success")

    else:
        return HttpResponse("error. you should only be sending a POST request here")


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
            print(search)

            search.save()

            return HttpResponse("Created new search!")
    else:
        return HttpResponse("Error")

@csrf_exempt
def validateUserContact(req):
    if req.method == 'POST':
        errors = FareSearch.objects.emailPhoneVal(req.POST)[1]
        user = FareSearch.objects.emailPhoneVal(req.POST)[0]
        if errors:
            return HttpResponse("Form error")

        elif len(user) > 0:
            return HttpResponse("User in DB")
        
        else:
            return HttpResponse("New user")
    else:
        return HttpResponse("Error")


@csrf_exempt
def updateFareSearch(req):
    print("updating fare search")
    if req.method == 'POST':
        parser = MyParser()
        parser.findWannaGetAway(req.POST['siteData'])
        
        if parser.averagePrice == "Error" or parser.lowestPrice == "Error":
            print("there's been an error with the parser")
            return HttpResponse("Failure")
        
        else:
            print("parser success!!")
            search = FareSearch.objects.get(id = req.POST['id'])
            search.updatedAt = datetime.now()

            AveragePrice.objects.create(
                search = search,
                price = parser.averagePrice
            )

            print(search.lowestPrice)

            if parser.lowestPrice < search.lowestPrice:
                search.lowestPrice = parser.lowestPrice
                sendLowPriceText(search)



            search.save()

            print(search.lowestPrice)

            return HttpResponse("Updated search query!")

    else:
        return HttpResponse("Error")

@csrf_exempt
def findSearches(req):
    if req.method == 'POST':
        response = {}
        searches = FareSearch.objects.filter(userPhone = req.POST['userPhone'])
        if len(searches) == 0:
            return HttpResponse("No searches found")
        
        else:

            for i in range(len(searches)):
                
                response[i] = [searches[i].originAirport, 
                                searches[i].destinationAirport, 
                                searches[i].departureDate, 
                                searches[i].returnDate]

            return JsonResponse(response)


    else:
        return HttpResponse("Error")



@csrf_exempt
def delete(req):
    if req.method == 'POST':
        
        searches = FareSearch.objects.filter(userPhone = req.POST['userPhone'])

        id = int(req.POST['searchID'])
        print('id requested is ', id, ' length of searches is ', len(searches))


        if (id > len(searches) - 1) or (id < 0):
            print("invalid!")
            return HttpResponse("Invalid search ID")
        

        else:
            searchToDelete = searches[id]

            searchToDelete.delete()

            return HttpResponse("Success")

    else:
        return HttpResponse('Error')


def recheckFares(req):

    searches = FareSearch.objects.all()
    for search in searches:
        postData = {'originAirport' : search.originAirport,
                    'destinationAirport' : search.destinationAirport,
                    'departingDate' : search.departureDate,
                    'returningDate' : search.returnDate,
                    'id' : search.id}

        print("post data is ", postData)
        encoded = bytes( urllib.parse.urlencode(postData).encode() )

        result = urllib.request.urlopen('http://127.0.0.1:4000/recheckFares', encoded)


    return HttpResponse("Success!")


def recheckFareWithID(req, fareID):
    search = FareSearch.objects.get(id = fareID)

    postData = {'originAirport' : search.originAirport,
                    'destinationAirport' : search.destinationAirport,
                    'departingDate' : search.departureDate,
                    'returningDate' : search.returnDate,
                    'id' : search.id}

    print("post data is ", postData)
    encoded = bytes( urllib.parse.urlencode(postData).encode() )

    result = urllib.request.urlopen('http://127.0.0.1:4000/recheckFares', encoded)

    return HttpResponse("Success!")



def getAllSearchIDs(req):
    searchIDs = []
    searches = FareSearch.objects.all()
    for search in searches:
        print(search.id)
        searchIDs.append(search.id)
    
    return JsonResponse(searchIDs, safe = False)


def sendLowPriceText(search):
    print('sending a txt message request to node')
    postData = {'userPhone' : search.userPhone,
                'userEmail' : search.userEmail,
                'originAirport' : search.originAirport,
                'destinationAirport' : search.destinationAirport,
                'departingDate' : search.departureDate,
                'returningDate' : search.returnDate}

    encoded = bytes( urllib.parse.urlencode(postData).encode() )
    result = urllib.request.urlopen('http://southwest.ben-bauer.net/sendLowPriceText', encoded)
    print(result.read())    
