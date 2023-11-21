from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.urls
from . import views

urlpatterns = [

    path('agenthome', views.agenthome, name='agenthome'),
    path('agentsearchflights', views.agentsearchflights, name='agentsearchflights'),
    path('agent_search_results', views.agent_search_results, name = 'agent_search_results'),
    path('agentpurchaseticket', views.agentpurchaseticket, name='agentpurchaseticket'),
    path('viewcommission', views.viewcommission, name='viewcommission'),
    path('viewtopcustomers', views.viewtopcustomers, name='viewtopcustomers'),

]
