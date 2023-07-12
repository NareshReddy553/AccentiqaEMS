from django.db import models
from django.utils.translation import gettext as _

# Create your models here.

class Employees(models.Model):
    emp_id = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(db_column='Phone_number', max_length=100, blank=True, null=True)  # Field name made lowercase.
    status = models.IntegerField(db_column='Status')  # Field name made lowercase.
    email = models.CharField(db_column='Email', unique=True, max_length=100)  # Field name made lowercase.
    created_user = models.IntegerField(blank=True, null=True)
    modified_user = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Employees'
        unique_together = ["first_name", "last_name"]


class EmployePasswords(models.Model):
    emp_password_id = models.IntegerField(primary_key=True)
    # emp_id = models.IntegerField()
    emp=models.ForeignKey("Employees", verbose_name=_(""), on_delete=models.CASCADE, related_name="emp_passwrd")
    password = models.CharField(max_length=200)
    created_user = models.IntegerField(blank=True, null=True)
    modified_user = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employe_passwords'
