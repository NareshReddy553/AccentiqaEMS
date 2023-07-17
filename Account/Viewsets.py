from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max, Q
from Account.models import Project, Users
from Account.serializers import ProjectSerializer, UsersSerializer

from Account.services import AllRecordsPagination


class UsersViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    pagination_class = AllRecordsPagination
    
    
class ProjectViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    pagination_class = AllRecordsPagination
    
    def get_queryset(self):
        company = self.request.headers.get("company")
        queryset = Project.objects.filter(
            company_id=company,
            is_active=True
        )
        return queryset