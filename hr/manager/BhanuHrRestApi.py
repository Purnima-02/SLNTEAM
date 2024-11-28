from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404,HttpResponse
from .models import *
from rest_framework.permissions import IsAuthenticated
from .BhanuHrSerializers import DSAApplicationsSerializer,FranchiseSerializer,SalesSerializer





class FranchiseModelViewSet(viewsets.ModelViewSet):
    queryset = franchise.objects.all()
    serializer_class = FranchiseSerializer
    
    # Franchise MyProfile Logic........................................
    @action(detail=True, methods=['post'])
    def franchiseMyProfile_update(self, request, pk=None):
        # print("post")
        # Get the instance
        instance = get_object_or_404(franchise,franchise_id=pk)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def franchiseMyProfile_get(self,request,pk=None):
        print("get")
        instance = franchise.objects.filter(franchise_id=pk).values()
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return HttpResponse("No dtaa")
        
        

class MyModelViewSet(viewsets.ModelViewSet):
    queryset = dsa.objects.all()
    serializer_class = DSAApplicationsSerializer
    # permission_classes = [IsAuthenticated]
    

    # Custom method for updating a record
    @action(detail=True, methods=['post'])
    def custom_update(self, request, pk=None):
        print("post")
        # Get the instance
        instance = get_object_or_404(dsa,dsa_registerid=pk)
        
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['get'])
    def custom_get(self,request,pk=None):
        print("get")
        instance = dsa.objects.filter(dsa_registerid=pk).values()
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return HttpResponse("No dtaa")
        
        
    @action(detail=False, methods=['get'])
    def custom_giveRefCodeFranCodeAll(self,request,pk=None):
        print("get")
        instance = dsa.objects.filter(approval_status="approved").values('dsa_registerid','dsa_name')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
        
    #  Franchise DSA's Ids.........
    @action(detail=True, methods=['get'])
    def giveFranchiseDSAIds(self,request,pk=None):
        # print("get")
        instance = dsa.objects.filter(franchiseCode=pk,approval_status="approved").values('dsa_registerid')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
# Franchise Sales Ids.........
    @action(detail=True, methods=['get'])
    def giveFranchiseSalesIds(self,request,pk=None):
        # print("get")
        instance = franchisesales.objects.filter(franchiseCode=pk,approval_status="approved").values('registerid')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
    @action(detail=True, methods=['get'])
    def sales_profile(self,request,pk=None):
        print("get")
        instance = franchisesales.objects.filter(registerid=pk).values()
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return HttpResponse("No dtaa")
        
    
    @action(detail=True, methods=['get'])
    def custom_giveRefCodeFranCode(self,request,pk=None):
        print("get")
        instance = dsa.objects.filter(dsa_registerid=pk,approval_status="approved").values('dsa_registerid','dsa_name')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
        
    # Franchise login......................................
    @action(detail=True, methods=['get'],url_path='(?P<second>.+)/custom_giveFranCode')
    def custom_giveFranCode(self,request,pk=None,second=None):
        # print(second)
        # print("getFranc Pass")
        instance = FranchiseUsers.objects.filter(franchise_id=pk,password=second)
        
        if instance.exists():
             return Response(status=200)
        else:
            return Response(status=404)
        
        
    
    # DSA Login......................................
    @action(detail=True, methods=['get'],url_path='(?P<second>.+)/dsaLoginCheck')
    def dsaLoginCheck(self,request,pk=None,second=None):
        # print(second)
        # print("get")
        instance = DSAUsers.objects.filter(dsa_registerid=pk,dsa_password=second).values('franchiseCode')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
    
     # SALES Login......................................
    @action(detail=True, methods=['get'],url_path='(?P<second>.+)/salesLoginCheck')
    def salesLoginCheck(self,request,pk=None,second=None):
        print(second)
        print("get")
        instance = Sales.objects.filter(registerid=pk,password=second).values('franchiseCode')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
    
    
    

    # Super Admin get All dsaids...........................
    
    @action(detail=False, methods=['get'])
    def giveAllDSAIds(self,request):
        print("get")
        instance = dsa.objects.filter(approval_status="approved").values('dsa_registerid','franchiseCode')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
    
    @action(detail=False, methods=['get'])
    def giveAllFranchiseIds(self,request):
        print("get")
        instance = franchise.objects.filter(aproval_status="approved").values('franchise_id')
        print(instance)
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
    
    @action(detail=False, methods=['get'])
    def giveAllSALESIds(self,request):
        print("get")
        instance = franchisesales.objects.filter(approval_status="approved").values('registerid','franchiseCode')
        
        if instance.exists():
             return Response(list(instance), status=200)
        else:
            return Response(status=404)
        
class SalesViewSet(viewsets.ModelViewSet):
    queryset = franchisesales.objects.all()
    serializer_class = SalesSerializer
    
        
        
    
         
        
        