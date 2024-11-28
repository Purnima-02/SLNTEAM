from rest_framework import serializers
from .models import *

class InputWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model=InputWindow
        fields='__all__'

class DisbursementOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disbursement
        fields='__all__'

class DisbursementDataSerializer(serializers.ModelSerializer):
    class Meta:
        model=DisbursementData
        fields='__all__'

class DisbursmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Disbursement
        fields='__all__'

class SettlementWindowSerializer(serializers.ModelSerializer):
    class Meta:
        model=SettlementWindow
        fields='__all__'
