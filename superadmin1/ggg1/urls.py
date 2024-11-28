from django.urls import path,include
from .views import *
from rest_framework.routers import DefaultRouter
from ggg1.restApi import hrViewSet



router = DefaultRouter()
router.register(r'mymodel',hrViewSet)

urlpatterns = [
path('customer',customersupport,name='customer'),
path('customers',customersupport1,name='customers'),
path('customerss',customersupport2,name='customerss'),
# dsa
path('customer1',customersupport3,name='customer1'),
path('customers2',customersupport4,name='customers2'),
path('customerss3',customersupport5,name='customerss3'),
# franchise
path('customer4',customersupport6,name='customer4'),
path('customers5',customersupport7,name='customers5'),
path('customerss6',customersupport8,name='customerss6'),
# hr
path('hrform/',hr_credentials_view,name='hrform'),
path('hr-credentials/',hr_credentials_views, name='hr_credentials_table'),
]