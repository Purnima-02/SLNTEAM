from rest_framework import serializers
from .models import *



class Ticketserializers(serializers.ModelSerializer):
    class Meta:
        model=Ticket
        fields='__all__'


class DSATicketserializers(serializers.ModelSerializer):
    class Meta:
        model=DSATicket
        fields='__all__'



class FranchiseeTicketserializers(serializers.ModelSerializer):
    class Meta:
        model=FranchiseeTicket
        fields='__all__'

