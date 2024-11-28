from rest_framework import viewsets,status
from manager.hrserializers import *
from .models import *
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password



class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    @action(detail=True, methods=['post'], url_path='loginCheck')
    def LoginCheck(self, request, pk=None):
        password = request.data.get('password')

        if not password:
            return Response({'error': 'Password is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Retrieve the employee based on employee_id (which is a string)
            employee = Employee.objects.get(employee_id=pk)

            if check_password(password, employee.password):
                serializer = EmployeeSerializer(employee)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except Employee.DoesNotExist:
            return Response({'error': 'Employee not found'}, status=status.HTTP_404_NOT_FOUND)



class FranchiseViewSet(viewsets.ModelViewSet):
    queryset = franchise.objects.all()
    serializer_class = FranchiseSerializer

    @action(detail=False, methods=['get'])
    def approve_records(self, request):
        # Filter the records where approval_status is 'approved'
        approved_records = franchise.objects.filter(aproval_status='approved')
        
        # Perform an action with the approved records; for example, you could return them
        if approved_records.exists():
            serializer = self.get_serializer(approved_records, many=True)
            return Response(serializer.data)
        else:
            return Response({"message": "No approved records found."})



class dsaViewSet(viewsets.ModelViewSet):
    queryset = dsa.objects.all()
    serializer_class = dsaSerializer

    