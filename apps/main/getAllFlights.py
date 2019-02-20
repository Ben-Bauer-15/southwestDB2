#!/usr/bin/env python3

import urllib.request
import urllib.parse
import time as _t
import json

def getAllFlightSearches():
    result = urllib.request.urlopen('http://18.188.177.136/generateSearches')
    
    searches = json.loads(result.read().decode('utf-8'))


# change back to for i in range(len(searches)):
    for i in range(len(searches)):
        search = searches[i]
        print('search object is ', search)
        orig = search[0][0]
        dest = search[0][1]

# change back to for j in range(len(search[1])):
        for j in range(len(search[1])):
            date = search[1][j]

            verificationData = {
                'originAirport' : orig,
                'destinationAirport' : dest,
                'departingDate' : date,
                'tripType' : 'oneWay'
            }

            verificationEncoded = bytes( urllib.parse.urlencode(verificationData).encode() )
            verificationReq = urllib.request.urlopen('http://18.188.177.136/verifyTrip', verificationEncoded)


            if verificationReq.read().decode('utf-8') == 'True':
                print("No searches!")


                try:
                    nodeRequest = urllib.request.urlopen('http://southwest.ben-bauer.net/startFareSearch', verificationEncoded)

                    verificationData['SWContent'] = json.loads(nodeRequest.read().decode('utf-8'))['message']
                    verificationEncoded = bytes( urllib.parse.urlencode(verificationData).encode() )
                    

                    djangoRequest = urllib.request.urlopen('http://18.188.177.136/postFlightData', verificationEncoded)

                    print(djangoRequest.read())
                
                except:
                    print('something went wrong')
                    pass

            else:
                print('search already exists')
                pass

getAllFlightSearches()