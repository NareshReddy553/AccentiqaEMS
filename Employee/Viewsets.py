from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max, Q

from Account.services import AllRecordsPagination
from Employee.models import Employees, Salary
from Employee.serializers import EmpSalarySerializer, EmployeesSerializer, EmployeesalariesSerializer, SalarySerializer


class EmployeesViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    pagination_class = AllRecordsPagination
    
    @action(detail=True, methods=['get'],url_path="empsal",serializer_class=EmployeesalariesSerializer)
    def set_password(self, request, pk=None):
        obj = self.get_object()
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

class SalaryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    pagination_class = AllRecordsPagination
    
    
    