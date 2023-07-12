

from django.urls.conf import path
from django.conf.urls import include, url
from rest_framework import routers

from Account.Viewsets import UsersViewset

router = routers.DefaultRouter()
router.register(r"users", UsersViewset, basename="users")

urlpatterns = [
        
    url("", include(router.urls)),
]