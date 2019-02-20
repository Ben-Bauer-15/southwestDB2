from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test$', views.test),
    url(r'^startFareSearch$', views.startFareSearch),
    url(r'^validate$', views.validateUserContact),
    url(r'^updateFareSearch$', views.updateFareSearch),
    url(r'^findSearches$', views.findSearches),
    url(r'^delete$', views.delete),
    url(r'^allSearches$', views.getAllSearches),
    url(r'^allSearchIDs$', views.getAllSearchIDs),
    url(r'^recheckFareWithID/(?P<fareID>\d+)$', views.recheckFareWithID),
    url(r'^postFlightData$', views.postFlightData),
    url(r'^generateSearches$', views.generateSearches),
    url(r'^getAllTrips$', views.getAllTrips),
    url(r'^getTripsByOrig/(?P<orig>\w+)$', views.getTripsByOrig),
    url(r'^getTripsByDest/(?P<dest>\w+)$', views.getTripsByDest),
    url(r'^getTripsByDate/(?P<year>\d+)/(?P<month>\d+)/(?P<date>\d+)$', views.getTripsByDate),
    url(r'^getTripsByOrigAndDest/(?P<orig>\w+)/(?P<dest>\w+)$', views.getTripsByOrigAndDest),
]