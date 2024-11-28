from rest_framework import serializers
from .models import *

class EmployeeSerializer(serializers.ModelSerializer):  

    class Meta:
        model = Employee
        fields = '__all__'

class FranchiseSerializer(serializers.ModelSerializer):

    class Meta:
        model = franchise
        fields = '__all__'   
class dsaSerializer(serializers.ModelSerializer):

    class Meta: 
        model = dsa
        fields = '__all__'             