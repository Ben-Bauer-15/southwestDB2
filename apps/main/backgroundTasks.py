import urllib.request
import time as _t
import json

def recheckFares():
    for i in range(5):
        result = urllib.request.urlopen('http://localhost:8000/allSearchIDs')
        ids = json.loads(result.read().decode('utf-8'))
        for searchId in ids:
            # print(searchId)
            result = urllib.request.urlopen('http://localhost:8000/recheckFareWithID/' + str(searchId))
            print(result.read())
        print("sleeping for 5 seconds")
        _t.sleep(5)

recheckFares()