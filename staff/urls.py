from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import accounts.urls
from . import views

urlpatterns = [

    path('staffhome', views.staffhome, name='staffhome'),
    path('staff_search_results', views.staff_search_results, name='staff_search_results'),
    path('staff_viewcustomers', views.staff_viewcustomers, name='staff_viewcustomers'),
    path('createnewflights', views.createnewflights, name='createnewflights'),
    path('addflight', views.addflight, name='addflight'),
    path('changestatus', views.changestatus, name='changestatus'),
    path('update_status', views.update_status, name='update_status'),
    path('addnewairplane', views.addnewairplane, name='addnewairplane'),
    path('confirmation_new_airplane', views.confirmation_new_airplane, name='confirmation_new_airplane'),
    path('addnewairport', views.addnewairport, name='addnewairport'),
    path('airport_add', views.airport_add, name='airport_add'),
    path('viewbookingagents', views.viewbookingagents, name='viewbookingagents'),
    path('addnewbookingagent', views.addnewbookingagent, name='addnewbookingagent'),
    path('add_agent', views.add_agent, name='add_agent'),
    path('viewfreqcustomers', views.viewfreqcustomers, name='viewfreqcustomers'),
    path('customerhistory', views.customerhistory, name='customerhistory'),
    path('revenue_comparison', views.revenue_comparison, name='revenuecomparison'),
    path('newpermission', views.newpermission, name='newpermission'),
    path('changepermission', views.changepermission, name='changepermission'),
    path('viewreports', views.viewreports, name='viewreports'),

]
