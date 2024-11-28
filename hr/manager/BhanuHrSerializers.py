from rest_framework import serializers
from .models import *





class DSAApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=dsa
        fields='__all__'
        
    # def to_representation(self, instance):
    #     # Get the original serialized data
    #     data = super().to_representation(instance)
        
    #     data['dsa_register'] = data.pop('dsa_registerid')
        
    #     return data
        
class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=franchise
        fields='__all__'
        
class SalesSerializer(serializers.ModelSerializer):
    class Meta:
      model=franchisesales
      fields='__all__'
      
# LoGiNS Serializers..

class FranchiseLoginSerializer(serializers.ModelSerializer):
    class Meta:
      model=FranchiseUsers
      fields='__all__'