from django.urls import path , include
from .views import *
from SmAdmin.views import *
from SmAdmin.Restapi import franchiseViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'branch',franchiseViewSet)




urlpatterns = [
    
    path('edu',hrEduViewsets, name='supedu'),
    path('goldloan',hrgoldapi, name='supGoldLoan'),
    path('laploan',hrlapapi, name='supLaploan'),
    path('plloan',hrplapi, name='supplloan'),
    path('hlloan',hrhlapi, name='suphlloan'),
    path('eduloan',hrBusiViewsets, name='supeduloan'),
    path('carloan',hrddproject, name='supcarloan'),
    path('credit',hrapi_credit_appli, name='supcredit'),
    path('otherloan',hrotherapi, name='supotherloan'),
    path('allinsurance',hrviewinsurance, name='supallinsurance'),
    path('lifeinsurance',hrviewlifeinsurance, name='suplifeinsurance'),
    path('geninsurance',hrviewgeninsurance, name='supgeninsurance'),
    path('hrhealthinsurance/',hrviewhealthinsurance, name='suphealthinsurance'),
    #anusha
    path('franchise/', hrfranchise_view,name='hrfranchise'),
    path('approve/<int:employee_id>/', approve_employee, name='approve_employee'),
    path('approved-franchises/', approved_franchises, name='approved_franchises'),
    path('reject/<int:employee_id>/', reject_employee, name='reject_employee'),
    path('rejected-franchises/', rejected_franchises, name='rejected_franchises'),
    path('approverecords/',franchiseViewSet.as_view({'get':'approve_records'}),name='approverecords'),


    path("",include)
]


