from rest_framework import serializers
from .models import *


class SuperAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuperAdmin
        fields='__all__'



class SuperAdminApplicationsSerializer(serializers.ModelSerializer):
    class Meta:
        model=SuperAdminApplications
        fields='__all__'
        

class DSAMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=DSAMasterData
        fields='__all__'
        
class FranchiseMasterDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=FranchiseMasterData
        fields='__all__'