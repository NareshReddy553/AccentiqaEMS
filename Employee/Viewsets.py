from datetime import datetime
from dateutil.parser import parse
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
    
    def __calculte_days(self,startdate,enddate):
        if  isinstance(enddate,str):
           enddate=parse(enddate)
        delta=enddate-parse(startdate)
        return delta.days
    
    def __get_total_amount(self,startdate,enddate,sal):
        days=self.__calculte_days(startdate,enddate)
        oneday_sal=sal%30
        return oneday_sal*days
        
    
    @action(detail=True, methods=['get'],url_path="empsal",serializer_class=EmployeesalariesSerializer)
    def employeesalary(self, request, pk=None):
        obj = self.get_object()
        billing_amount=0
        non_billing_amount=0
        
        
        serializer = self.get_serializer(obj)
        
        
        for data in serializer.data.get('salary'):
            enddate=data.get('enddate')
            if not enddate:
                enddate=datetime.today()
            if data['isbillable']:
                amount=self.__get_total_amount(data.get('startdate',datetime.today()),enddate,data['salary'])
                billing_amount+=amount
            else:
                amount=self.__get_total_amount(data.get('startdate',datetime.today()),enddate,data['salary'])
                non_billing_amount+=amount
                
        final_data=serializer.data
        final_data['chart']={
            "billing_amount":billing_amount,
            "nonbilling_amount":non_billing_amount
        }
        
        return Response(final_data,status=status.HTTP_200_OK)



class SalaryViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    pagination_class = AllRecordsPagination
    
    
    