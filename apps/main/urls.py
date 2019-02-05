from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test$', views.test),
    url(r'^parserTest', views.parserTest),
    url(r'startFareSearch', views.startFareSearch)
]