from django.urls.conf import path
from django.conf.urls import include, url
from rest_framework import routers

from Employee.Viewsets import EmployeesViewset, SalaryViewset

router = routers.DefaultRouter()
router.register(r"empolyees", EmployeesViewset, basename="incidents")
router.register(r"salary", SalaryViewset, basename="salaries")
urlpatterns = [
        
    url("", include(router.urls)),
]