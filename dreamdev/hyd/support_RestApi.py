from rest_framework import viewsets
from rest_framework.response import Response
from .support_serializers import Ticketserializers, DSATicketserializers,FranchiseeTicketserializers
from .models import Ticket, DSATicket,FranchiseeTicket,custmer


class Ticketviewsets(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = Ticketserializers

class DSATicketviewsets(viewsets.ModelViewSet):
    queryset = DSATicket.objects.all()
    serializer_class = DSATicketserializers


def getByRegisterId(self,request,name):
     try:
        queryset = custmer.objects.filter(name=name)
        if queryset.exists():
            serializer = self.get_serializer(many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message": "No records found"}, status=404)
     except Exception as e:
        return Response({"error": str(e)}, status=500)

    
class FranchiseeTicketviewsets(viewsets.ModelViewSet):
    queryset = FranchiseeTicket.objects.all()
    serializer_class = FranchiseeTicketserializers

