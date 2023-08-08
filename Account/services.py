
import pandas as pd
from collections import OrderedDict
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from django.core.cache import cache
from .models import Users
from rest_framework.exceptions import ValidationError

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



def read_xls_file(file, field_names):
    try:
        df = pd.read_excel(
            file,
            header=[0],
            names=list(field_names.keys()),
            dtype=field_names,
        )
    except Exception as e:
        raise ValidationError(
            detail={"Error": e},
        )

    if df.empty:
        raise ValidationError({"Error": "File containes zero records"}, "empty_file")
    # # fillna() is used replace empty values with string
    # df["tfn"] = df["tfn"].str.strip()
    # df["did"] = df["did"].str.strip()
    # df["did_spanish"] = df["did_spanish"].str.strip()
    # df["callcenter"] = df["callcenter"].str.strip()
    # values = {"tfn": "", "did": "", "did_spanish": "", "callcenter": "", "isactive": ""}
    # tfn_dict = df.fillna(value=values).to_dict("records")
    emp_dict=df.to_dict('records')
    # for i in emp_dict:
    #     if not str(i["isactive"]):
    #         i["isactive"] = 1
    #     elif i["isactive"] == "Y":
    #         i["isactive"] = 1
    #     elif i["isactive"] == "N":
    #         i["isactive"] = 0
    return emp_dict