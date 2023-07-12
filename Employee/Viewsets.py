from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max, Q

from Account.services import AllRecordsPagination
from Employee.models import Employees
from Employee.serializers import EmployeesSerializer


class EmployeesViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Employees.objects.all()
    serializer_class = EmployeesSerializer
    pagination_class = AllRecordsPagination