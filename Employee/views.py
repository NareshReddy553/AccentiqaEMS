from datetime import datetime
from django import views
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import generics
from Account.models import Company, Project

from Employee.models import Employees, Salary
from Employee.serializers import EmployeesSerializer, EmployeestUploadSerializer, SalarySerializer
from Account.services import read_xls_file
from rest_framework.parsers import FormParser, MultiPartParser,FileUploadParser
from config import settings
from rest_framework.views import APIView
# Create your views here.


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def project_chart(request):
    chart_data=[]
    project=request.data.get('project',None)
    if not project:
        raise ValidationError({"Error":"project is required"})
    company=request.headers.get("company")
    if not company:
        raise ValidationError({"Error":"company is required"})
    
    chart_data=list(Salary.objects.filter(project_id=project,project__is_active=True,project__company_id=company).values('isbillable').annotate(Count('isbillable')).values('isbillable','isbillable__count'))
    
    return Response(chart_data, status=status.HTTP_200_OK)


class EmployeesUploadView(APIView):
    """
    post: Create a new document and a new document file.
    """
    serializer_class = EmployeestUploadSerializer
    permission_classes = (IsAuthenticated,)
    parser_classes=(MultiPartParser, FormParser,FileUploadParser)

    def post(self, request, format=None):
        serializer =self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            uploaded_file = serializer.validated_data['file']
            emp_data = read_xls_file(uploaded_file, settings.EMPLOYEE_EXCEL_FIELD_NAME)
            if emp_data:
            # Create Emp and Sal records from the Excel data
                for emp_info in emp_data:
                    company_obj=Company.objects.filter(
                            campany_name__icontains=emp_info.get('company')
                        ).first()
                    project_obj=Project.objects.filter(
                            project_name__icontains=emp_info.get('project'),
                            is_active=True
                        ).first()
                    
                    emp_info['project']=project_obj.pk
                    emp_info['company']=company_obj.pk
                    request.data.update(emp_info)
                    emp_serializer = EmployeesSerializer(context={"request":request},data=emp_info)
                    if emp_serializer.is_valid(raise_exception=True):
                        emp_instance = emp_serializer.save()  
                    else:
                        return Response(emp_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Data import successful"}, status=status.HTTP_201_CREATED)
        