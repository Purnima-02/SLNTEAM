from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404,HttpResponse
from .models import *
from rest_framework.permissions import IsAuthenticated
from SmAdmin.serializers import FranchiseSerializer


        
class franchiseViewSet(viewsets.ModelViewSet):
    queryset = franchise.objects.all()
    serializer_class = FranchiseSerializer

    @action(detail=False, methods=['get'])
    def approve_records(self, request):
        # Filter the records where approval_status is 'approved'
        approved_records = franchise.objects.filter(aproval_status='approved')
        
        # Perform an action with the approved records; for example, you could return them
        if approved_records.exists():
            serializer = self.get_serializer(approved_records, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No approved records found."})

    
    
 
    

    