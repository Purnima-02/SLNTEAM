"""
URL configuration for accountsnew project.

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
from account import views
from account.accontapi import DisburseAppliViewsets,SettlementWindowViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('DisburseViewsets',DisburseAppliViewsets,basename='disburse')
router.register('SettlementWindowViewSet',SettlementWindowViewSet,basename='SettlementWindowViewSet')


urlpatterns = [
    path('fetch-data/', views.fetch_and_store_data, name='fetch_data'),
    path('view_details/', views.disbursement_list, name='view'),
    path('input-form/<int:disbursement_id>/',views.input_form, name='input_form'),
    path('view-input/<str:application_id>/', views.view_input_detail, name='view_input_detail'),
    path('output-form/<int:disbursement_id>/', views.output_form, name='output_form'),
    path('view-output/<str:application_id>/', views.view_output_detail, name='view_output_detail'),
    path('settle-form/<int:disbursement_id>/', views.settle_form, name='settle_form'),
    path('view-settle/<str:application_id>/', views.view_settle_detail, name='view_settle_detail'),
    path('dashboard/',views.dashboard,name='dash'),
    path('login/check/', views.login_check, name='login_check'),  # Route for the login API call
    path('logout/', views.logout_view, name='logout'),





    path("",include(router.urls)),

    path("getclaim/<str:refCode>",DisburseAppliViewsets.as_view({"get":"getClaimed"}),name="get-claim"),
    path("postAcnt",DisburseAppliViewsets.as_view({"post":"postMethod"}),name="post-claim"),
    path('getDisburseIds/<str:refCode>',DisburseAppliViewsets.as_view({'get':'getDisburseIds'}),name='getDisburseIds'),
    path('getDisburseRecords/<str:refCode>',DisburseAppliViewsets.as_view({'get':'getDisburseRecords'}),name='getDisburseRecords'),
       
    path('getFranchiseDisbursedRecords/<str:refCode>',DisburseAppliViewsets.as_view({'get':'getFranchiseDisbursedRecords'}),name='getFranchiseDisbursedRecords'),

    path('getFranchiseClaimed/<str:refCode>',DisburseAppliViewsets.as_view({'get':'getFranchiseClaimed'}),name='getFranchiseClaimed'),



    # path('getAccdata',get_all_dataAsJson,name='dtaa'),



]
