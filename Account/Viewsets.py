from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.db.models import Max, Q
from Account.models import Users
from Account.serializers import UsersSerializer

from Account.services import AllRecordsPagination


class UsersViewset(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    pagination_class = AllRecordsPagination