from datetime import datetime
from rest_framework import generics,viewsets,status
from .models import *
from account.accountserializers import DisbursmentSerializer,SettlementWindowSerializer
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Sum
from django.db.models import Q



class DisburseAppliViewsets(viewsets.ModelViewSet):
    queryset=Disbursement.objects.all()
    serializer_class=DisbursmentSerializer

# Get Claimed Records where isClaim is False...............
    def getClaimed(self,request,refCode):
         
     try:
        queryset = Disbursement.objects.filter(refCode=refCode,dsaIsClaim=False)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message": "No records found"}, status=404)
     except Exception as e:
        return Response({"error": str(e)}, status=500)
    
    
    def getFranchiseClaimed(self,request,refCode):
     try:
        queryset = Disbursement.objects.filter(franchiseIsClaim=False,franchCode=refCode)
        if queryset.exists():
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data,status=200)
        else:
            return Response({"message": "No records found"}, status=404)
     except Exception as e:
        return Response({"error": str(e)}, status=500)





# Update isClaimed To True when send claim request from dsa,franchise
    def postMethod(self,request):
      data=request.data
      print(data)
      
      print(data.get('referenceId'))
      refid=data.get('referenceId')
      
      if data.get('refCode'):
         ids=data.get('ids')
         Disbursement.objects.filter(application_id__in=ids).update(dsaIsClaim=True)
         DisbursementData.objects.filter(application_id__in=ids).update(refid=refid)
         return Response("Ok",status=200)
      else:
         ids=data.get('ids')
         Disbursement.objects.filter(application_id__in=ids).update(franchiseIsClaim=True)
         DisbursementData.objects.filter(application_id__in=ids).update(franchrefid=refid)

         return Response("Ok",status=200)

          

# getDisbursedRecordsIDS...................................
    def getDisburseIds(self, request, refCode):
     try:
        queryset = Disbursement.objects.filter(refCode=refCode).values('application_id')
        if queryset.exists():
            application_ids = list(queryset)  # Convert queryset to a list of dictionaries
            return Response(application_ids, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)
     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     


# For disbursed Totalamount and no of loans count.................
    def getDisburseRecords(self, request, refCode):#For DSA........
     try:
        queryset = Disbursement.objects.filter(refCode=refCode)
        if queryset.exists():
               serializer = self.get_serializer(queryset, many=True)
               return Response(serializer.data,status=200)
            
        else:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)
     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    def getFranchiseDisbursedRecords(self,request,refCode):
     try:
        queryset = Disbursement.objects.filter(franchCode=refCode,refCode=None)
        if queryset.exists():
               serializer = self.get_serializer(queryset, many=True)
               return Response(serializer.data,status=200)
            
        else:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)
     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
        
    
    
    
    
    @action(detail=False, methods=['post'])
    def calculateAllDisbursementAmountUsingIds(self,request):
        result=[]
        print(request.data)
        if request.data.get('date'):
         date=request.data.get('date')
         date_format = "%Y-%m-%d"
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         startDate = datetime.strptime(date1, date_format).date()
         endDate = datetime.strptime(date2, date_format).date()
         for i in request.data.get('ids'):
        #    print(i)
           totalDisb=Disbursement.objects.filter((Q(refCode=i) | Q(franchCode=i)),appliCreatedAt_gte=startDate,appliCreatedAt_lte=endDate).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
        
         print("All result is",result)
         return Response(result,status=200)
         
         
        for i in request.data.get('ids'):
           print(i,"from ids")
           totalDisb=Disbursement.objects.filter( Q(refCode=i) | Q(franchCode=i) ).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
           print(totalDisb)
        
        print("All result is",result)
        return Response(result,status=200)
        # print(ids)
        
        
    @action(detail=False, methods=['post'])
    def calculateAllFranchiseDisbursementAmountUsingIds(self,request):
        result=[]
        print(request.data)
        if request.data.get('date'):
         date=request.data.get('date')
         date_format = "%Y-%m-%d"
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         startDate = datetime.strptime(date1, date_format).date()
         endDate = datetime.strptime(date2, date_format).date()
         for i in request.data.get('ids'):
        #    print(i)
           totalDisb=Disbursement.objects.filter(refCode=None,franchCode=i,appliCreatedAt_gte=startDate,appliCreatedAt_lte=endDate).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
        
         print("All result is",result)
         return Response(result,status=200)
         
         
        for i in request.data.get('ids'):
           print(i,"from ids")
           totalDisb=Disbursement.objects.filter(refCode=None,franchCode=i).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
           print(totalDisb)
        
        print("All result is",result)
        return Response(result,status=200)
    
    
    
    
    @action(detail=False, methods=['post'])
    def calculateAllFranchiseClosedAmountUsingIds(self,request):
        result=[]
        # print([field.name for field in Disbursment._meta.get_fields()])
        print(request.data)
        if request.data.get('date'):
         date=request.data.get('date')
         date_format = "%Y-%m-%d"
         date1=date.split(' to ')[0]
         date2=date.split(' to ')[1]
         startDate = datetime.strptime(date1, date_format).date()
         endDate = datetime.strptime(date2, date_format).date()
         for i in request.data.get('ids'):
        #    print(i)
           totalDisb=Disbursement.objects.filter(franchCode=i,date_gte=startDate,date_lte=endDate).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
        
         print("All result is",result)
         return Response(result,status=200)
         
         
        for i in request.data.get('ids'):
           print(i,"from ids")
           totalDisb=Disbursement.objects.filter(franchCode=i).aggregate(total=Sum('disbursedAmount'))['total'] or 0
           result.append(totalDisb)
           print(totalDisb)
        
        print("All result is",result)
        return Response(result,status=200)
    
    
# SuperAdmin DashBoard TotalAmounts Functions..................

    def exceptSLNAllFranchiseTotalAmounts(self,request):
        print()
        
    
class SettlementWindowViewSet(viewsets.ModelViewSet):
    # print()
    queryset=SettlementWindow.objects.all()
    serializer_class=SettlementWindowSerializer
    
    @action(detail=True, methods=['get'])
    def getEarningRecordsOfDSA(self,request,pk):
     try:
        queryset = SettlementWindow.objects.filter(refCode=pk)
        if queryset.exists():
               serializer = self.get_serializer(queryset, many=True)
               return Response(serializer.data,status=200)
            
        else:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)
     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
    
    @action(detail=True, methods=['get'])
    def getEarningRecordsOfFranchise(self,request,pk):
     try:
        queryset = SettlementWindow.objects.filter(franchCode=pk)
        if queryset.exists():
               serializer = self.get_serializer(queryset, many=True)
               return Response(serializer.data,status=200)
            
        else:
            return Response({"message": "No records found"}, status=status.HTTP_404_NOT_FOUND)
     except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
