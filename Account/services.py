
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.core.cache import cache
from .models import Users

class AllRecordsPagination(LimitOffsetPagination):
    def paginate_queryset(self, queryset, request, view=None):
        self.limit = queryset.count()
        if self.limit is None:
            return None

        self.count = queryset.count()
        self.offset = 0
        self.request = request
        if self.count > self.limit and self.template is not None:
            self.display_page_controls = True

        if self.count == 0 or self.offset > self.count:
            return []
        return list(queryset[self.offset:self.offset + self.limit])

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.count),
            ('results', data)
        ]))





def get_cached_user(userid):
    if userid is None:
        return None
    user = cache.get("USER_" + str(userid))
    if user is None:
        user = Users.objects.values(
            "user_id", "email", "first_name", "last_name"
        ).filter(pk=userid).first()
        if user is not None:
            cache.set("USER_" + str(userid), user, 120)
    return user