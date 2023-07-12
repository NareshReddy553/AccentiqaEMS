from django.urls.conf import path
from django.conf.urls import include, url
from rest_framework import routers

from Employee.Viewsets import EmployeesViewset

router = routers.DefaultRouter()
router.register(r"empolyees", EmployeesViewset, basename="incidents")

urlpatterns = [
        
    url("", include(router.urls)),
]