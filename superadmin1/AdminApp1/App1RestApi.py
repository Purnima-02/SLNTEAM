
from django.shortcuts import render
from rest_framework import generics,viewsets,status

from AdminApp1.App1Seializers import SuperAdminSerializer,SuperAdminApplicationsSerializer,DSAMasterDataSerializer,FranchiseMasterDataSerializer
from .models import *
from rest_framework.response import Response




class AdminViewsets(viewsets.ModelViewSet):
    queryset=SuperAdmin.objects.all()
    serializer_class=SuperAdminSerializer

    

    def getByRegisterId(self,request,register_id):
     try:
        queryset = SuperAdmin.objects.filter(adminId=register_id)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message": "No records found"}, status=404)
     except Exception as e:
        return Response({"error": str(e)}, status=500)


class Admin_AppliViewsets(viewsets.ModelViewSet):
    queryset=SuperAdminApplications.objects.all()
    serializer_class=SuperAdminApplicationsSerializer
    

class DSAMasterData_AppliViewsets(viewsets.ModelViewSet):
    queryset = DSAMasterData.objects.order_by('-id')[:1]
    serializer_class=DSAMasterDataSerializer
    
class FranchiseMasterData_AppliViewsets(viewsets.ModelViewSet):
    queryset = FranchiseMasterData.objects.order_by('-id')[:1]
    serializer_class=FranchiseMasterDataSerializer

   

   