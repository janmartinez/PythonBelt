from django.contrib import admin
from django.urls import path, include
from travel_app import views
from django.conf.urls import url


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',views.index),
    url(r'^addUser$',views.addUser),
    url(r'^login$',views.login),
    url(r'^clear$',views.clear),
    url(r'^travels$',views.allTravels),
    url(r'^travels/add$',views.addTravel),
    url(r'^addnewtrip$',views.addnewtrip),
    url(r'^travels/destination/(?P<trips_id>\d+)$',views.tripinfo),
    url(r'^jointrip/(?P<trips_id>\d+)$',views.jointrip),

]