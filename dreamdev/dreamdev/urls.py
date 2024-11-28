"""
URL configuration for dreamdev project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""



from django.contrib import admin
from django.urls import path,include
from hyd import views
from rest_framework.routers import DefaultRouter
from hyd.support_RestApi import Ticketviewsets,DSATicketviewsets,FranchiseeTicketviewsets




router=DefaultRouter()
router.register('api_customer_ticket',Ticketviewsets,basename='api_customer_tic'),
router.register('api_DSA_ticket',DSATicketviewsets,basename='api_DSA_ticket'),
router.register('api_Franchisee_ticket',FranchiseeTicketviewsets,basename='api_Franchisee_ticket'),




urlpatterns = [
    path('admin/', admin.site.urls),
    path('ticket_create/<int:instance_id>',views.create_ticket,name='ticket_create'),
    path('ticket_create/', views.create_ticket, name='create_ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_details, name='ticket_details'),

    path('ticket/<int:ticket_id>/update_status/', views.update_ticket_status, name='update_ticket_status'),
    path('ticketview/',views.ticketview,name='ticketview'),
    path('ok/',views.ok, name='ok'),
    # path('dashbord/',views.dashboard, name='dashbord'),
    path('open_tickets/',views.open_tickets_view,name='open_tickets'),
    path('inprogress_tickets/',views.inprogress_tickets_view,name='inprogress_tickets'),
    path('resolved_tickets/',views.resolved_tickets,name='resolved_tickets'),


# /////////////////////////////////   DSA     ////////////////////////////////////
   

    path('DSA_create_ticket/<int:instance_id>',views.DSA_create_ticket,name='DSA_create_ticket'),
    path('DSA_create_ticket/', views.DSA_create_ticket, name='DSA_create_ticket'),
    path('DSAticket/<int:ticket_id>/', views.DSA_ticket_details, name='DSA_ticket_details'),

    path('ticket/<int:ticket_id>/DSA_update_status/', views.DSA_update_ticket_status, name='DSA_update_ticket_status'),
    path('DSA_ticketview/',views.DSA_ticketview,name='DSA_ticketview'),
    path('DSA_open_tickets_view/',views.DSA_open_tickets_view,name='DSA_open_tickets_view'),
    path('DSA_inprogress_tickets/',views.DSA_inprogress_tickets_view,name='DSA_inprogress_tickets_view'),
    path('DSA_resolved_tickets/',views.DSA_resolved_tickets,name='DSA_resolved_tickets'),






# # ///////////////////////////////////////     franchisee    //////////////////////


   
    path('Franchisee_create_ticket/<int:instance_id>',views.Franchisee_create_ticket,name='Franchisee_create_ticket'),
    path('Franchisee_create_ticket/', views.Franchisee_create_ticket, name='Franchisee_create_ticket'),
    path('Franchiseeticket/<int:ticket_id>/', views.Franchisee_ticket_details, name='Franchisee_ticket_details'),

    path('ticket/<int:ticket_id>/Franchisee_update_status/', views.Franchisee_update_ticket_status, name='Franchisee_update_ticket_status'),
    path('Franchisee_ticketview/',views.Franchisee_ticketview,name='franchisee_ticketview'),
    path('Franchisee_open_tickets_view/',views.Franchisee_open_tickets_view,name='Franchisee_open_tickets_view'),
    path('Franchisee_inprogress_tickets/',views.Franchisee_inprogress_tickets_view,name='Franchisee_inprogress_tickets_view'),
    path('Franchisee_resolved_tickets/',views.Franchisee_resolved_tickets,name='Franchisee_resolved_tickets'),









# ////////////////////////////     Dashboard       ///////////////////

    path('new_dashboard/',views.newdash, name='new_dashboard'),





    path('Customer_tickets/',views.Customer_tickets, name='Customer_tickets'),
    path('DSA_tickets/',views.DSA_tickets, name='DSA_tickets'),
    path('Franchisee_tickets/',views.Franchisee_tickets, name='Franchisee_tickets'),




        path('dashboard/',views.dash, name='dashboard'),


path('contact_table/',views.contactsupport,name='contact_table'),




path('login/check/', views.login_check, name='login_check'),  # Route for the login API call
path('logout/', views.logout_view,name='logout'),



path('',include(router.urls)),






 ]
