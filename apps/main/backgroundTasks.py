#!/usr/bin/python3

import urllib.request
import time as _t
import json

def activateFareChecking():
    result = urllib.request.urlopen('http://18.188.177.136/allSearchIDs')
    ids = json.loads(result.read().decode('utf-8'))
    for searchId in ids:
        # print(searchId)
        result = urllib.request.urlopen('http://18.188.177.136/recheckFareWithID/' + str(searchId))
        print(result.read())
    print("sleeping for 5 seconds")

recheckFares()