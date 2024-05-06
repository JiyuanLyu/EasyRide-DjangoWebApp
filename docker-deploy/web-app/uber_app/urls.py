from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    ## owner require a ride
    path('ride-request/', views.ride_request, name='ride_request'),
    path('register_user/', views.user_request, name='user_request'),
]
