from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^test$', views.test),
    url(r'startFareSearch', views.startFareSearch),
    url(r'validate', views.validateUserContact)
]