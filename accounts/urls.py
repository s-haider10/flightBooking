from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('search_flight', views.search_flight, name='search_flight'),
    path('search_for_flight', views.search_for_flight, name='search_for_flight'),
    path('flightstatus', views.flightstatus, name='flightstatus'),
    path('checkstatus', views.checkstatus, name='checkstatus'),
    path('customersignup', views.customersignup, name='customersignup'),
    path('staffsignup', views.staffsignup, name='staffsignup'),
    path ('agentsignup', views.agentsignup, name='agentsignup'),
    path('logout', views.logout, name='logout'),
    path('customerhome', views.acustomerhome, name='customerhome'),
    path('agenthome', views.aagenthome, name='agenthome'),
    path('staffhome', views.astaffhome, name='staffhome'),
]
