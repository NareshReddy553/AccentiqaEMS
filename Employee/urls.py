from django.urls.conf import path
from django.conf.urls import include, url
from rest_framework import routers

from Employee.Viewsets import EmployeesViewset, SalaryViewset
from Employee.views import project_chart

router = routers.DefaultRouter()
router.register(r"empolyees", EmployeesViewset, basename="emp")
router.register(r"salary", SalaryViewset, basename="salaries")
urlpatterns = [
    path("project/projectchart",project_chart),
    url("", include(router.urls)),
]