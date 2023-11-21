from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.urls
from . import views


urlpatterns = [
    path('customerhome', views.customerhome, name='customerhome'),
    path('customer_search_flight', views.customer_search_flight, name='customer_search_flight'),
    path('customer_search_results', views.customer_search_results, name='customer_search_results'),
    path('purchaseticket', views.purchaseticket, name='purchaseticket'),
    path('trackmyspending', views.trackmyspending, name='trackmyspending'),

]
