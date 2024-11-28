# urls.py
from django.urls import path, include
from . import views
from .hrapi import *
from rest_framework.routers import DefaultRouter





router = DefaultRouter()
router.register(r'franchises', FranchiseViewSet)
router.register(r'approval', dsaViewSet)


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    # path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('success/<str:employee_id>/<str:password>/<str:employee_type>/',views.success, name='success'),
    path('count/', views.hr_dashboard_view, name='count'),
    path('dsa/', views.hrdsaview, name='hrdsa'),
    path('lists/<int:employee_id>',views.lists,name='lists'),

    

    path('approve/<int:employee_id>/', views.approve_employee, name='approve_employee'),
    path('approved-franchises/', views.approved_franchises, name='approved_franchises'),
    path('reject/<int:employee_id>/', views.reject_employee, name='reject_employee'),
    path('rejected-franchises/', views.rejected_franchises, name='rejected_franchises'),
    
    path('okfranchises/', views.approvedfranchises, name='okfranchises'),


    path('dsa-approve/<int:employee_id>/', views.dsa_approve, name='dsa_approve'),
    path('dsa-approved/', views.approved, name='dsapproved'),
    path('dsa-reject/<int:employee_id>/', views.dsa_reject, name='dsa_reject'),
    path('dsa-rejected/', views.dsa_rejected, name='dsa_rejected'),
         

         
    path('franchise/', views.hrfranchise_view,name='hrfranchise'),
    path('Edu/', views.hrEduViewsets,name='hredu'),
    path('goldloan/', views.hrgoldapi,name='hrGoldLoan'),
    path('laploan/', views.hrlapapi,name='hrLaploan'),
    path('plloan/', views.hrplapi,name='hrplloan'),
    path('hlloan/', views.hrhlapi,name='hrhlloan'),
    path('busloan/', views.hrBusiViewsets,name='hrbusloan'),
    path('carloan/', views.hrddproject,name='hrcarloan'),
    path('credit/', views.hrapi_credit_appli, name='credit'),
    path('otherloan/', views.hrotherapi, name='hrotherloan'),
    path('allinsurance/', views.hrviewinsurance, name='allinsurance'),
    path('lifeinsurance/', views.hrviewlifeinsurance, name='lifeinsurance'),
    path('geninsurance/', views.hrviewgeninsurance, name='geninsurance'),
    path('hrhealthinsurance/', views.hrviewhealthinsurance, name='hrhealthinsurance'),
    path('employees/', views.employee_list, name='employee_list'),
    path('franchises/', views.franchise_list, name='franchise_list'),
    path('dsas/', views.dsa_list, name='dsa_lists'),
    path('sales/', views.sales_list, name='sales_list'),
    path('hrlogin/', views.hrLogin, name='hrlogin'),




    # login and register
    path('register_sales/', views.register_sales, name='register_sales'),
    path('register_dsa_user/', views.register_dsa_user, name='register_dsa_user'),
    path('register_franchise_user/', views.register_franchise_user, name='register_franchise_user'),
    path('register_customer/', views.register_customer, name='register_customer'),

  
    path("",include(router.urls)),
    path('dsa/<str:dsa_registerid>/', dsaViewSet.as_view({'get': 'get_by_registerid'}), name='dsa-get-by-registerid'),
    #anusha
    # path('employee/<str:pk>/loginCheck/', EmployeeViewSet.as_view({'post': 'LoginCheck'}), name='employee-login-check'),
    path('branch/agreerecords/',FranchiseViewSet.as_view({'get':'approve_records'}),name='approverecords')


    # path('api/approve/<int:employee_id>/', views.approve_employee, name='api_approve_employee'),
    # path('api/approved-franchises/', views.approved_franchises, name='api_approved_franchises'),



     

]




