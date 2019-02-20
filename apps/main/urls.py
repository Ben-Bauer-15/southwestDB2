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
    url(r'^recheckFares', views.recheckFares),
    url(r'^allSearchIDs', views.getAllSearchIDs),
    url(r'recheckFareWithID/(?P<fareID>\d+)$', views.recheckFareWithID),
]