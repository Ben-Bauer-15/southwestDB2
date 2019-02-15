import urllib.request
import time as _t

def recheckFares():
    result = urllib.request.urlopen('http://localhost:8000/recheckFares')
    print(result.read())
    _t.sleep(2)

recheckFares()