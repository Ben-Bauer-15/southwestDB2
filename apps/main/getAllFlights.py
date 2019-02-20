#!/usr/bin/python3

import urllib.request
import urllib.parse
import time as _t
import json

def getAllFlightSearches():
    result = urllib.request.urlopen('http://18.188.177.136/generateSearches')
    
    searches = json.loads(result.read().decode('utf-8'))

    for i in range(5):
        search = searches[i]
        orig = search[0][0]
        dest = search[0][1]

        for j in range(5):
            date = search[1][j]
            nodePostData = {
                'originAirport' : orig,
                'destinationAirport' : dest,
                'departingDate' : date,
                'tripType' : 'oneWay'
                }

            nodeEncoded = bytes( urllib.parse.urlencode(nodePostData).encode() )
            nodeRequest = urllib.request.urlopen('http://southwest.ben-bauer.net/startFareSearch', nodeEncoded)


            djangoPostData = {
                'destinationAirport' : dest,
                'originAirport' : orig,
                'date' : date,
                'SWContent' : json.loads(nodeRequest.read().decode('utf-8'))['message']
            }

            djangoEncoded = bytes( urllib.parse.urlencode(djangoPostData).encode() )
            djangoRequest = urllib.request.urlopen('http://18.188.177.136/postFlightData', djangoEncoded)

            print(djangoRequest.read())
            

getAllFlightSearches()