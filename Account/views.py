from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from Account.models import Company
from rest_framework import status

from Account.serializers import CompanySerializer
# Create your views here.

@api_view(['GET'])
@permission_classes([])
def get_companies(request):
    # company=request.headers.get("company")
    try:
        serializer = CompanySerializer(Company.objects.all(),many=True)
    except Exception as e:
        return e
    return Response(serializer.data, status=status.HTTP_200_OK)
