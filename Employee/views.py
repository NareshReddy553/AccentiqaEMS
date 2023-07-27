from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count

from Employee.models import Salary

# Create your views here.


@api_view(["GET"])
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