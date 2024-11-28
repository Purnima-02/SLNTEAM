from rest_framework import serializers
from SmAdmin.models import *

class FranchiseSerializer(serializers.ModelSerializer):
    class Meta:
        model=franchise
        fields='__all__'