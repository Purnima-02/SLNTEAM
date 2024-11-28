from rest_framework import serializers
from .models import *



class HRSerializer(serializers.ModelSerializer):
    class Meta:
      model=HRCredentials
      fields='__all__'