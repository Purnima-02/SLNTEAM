from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404,HttpResponse
from .models import *
from rest_framework.permissions import IsAuthenticated
from ggg1.serializers import HRSerializer


        
class hrViewSet(viewsets.ModelViewSet):
    queryset = HRCredentials.objects.all()
    serializer_class = HRSerializer
    
    
 
    @action(detail=True, methods=['get'], url_path='(?P<email>.+)/(?P<second>.+)/hrLoginCheck')
    def hrLoginCheck(self, request,pk=None, email=None, second=None):


        instance = HRCredentials.objects.filter(email=email, password=second)
    
        if instance.exists():
            return Response(status=200)
        else:

            return Response(status=500)

    