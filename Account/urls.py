

from django.urls.conf import path
from django.conf.urls import include, url
from rest_framework import routers

from Account.Viewsets import ProjectViewset, UsersViewset
from Account.views import get_companies

router = routers.DefaultRouter()
router.register(r"users", UsersViewset, basename="users")
router.register(r"projects", ProjectViewset, basename="projects")

urlpatterns = [
    path("company/companies",get_companies),
    url("", include(router.urls)),
]