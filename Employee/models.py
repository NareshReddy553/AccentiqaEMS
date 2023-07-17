from django.db import models
from django.utils.translation import gettext as _

from Account.models import Company, Users,Project

# Create your models here.

class Employees(models.Model):
    emp_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    phone_number = models.CharField(db_column='Phone_number', max_length=100, blank=True, null=True)  
    status = models.IntegerField(db_column='Status', default=-1)  
    email = models.CharField(db_column='Email', unique=True, max_length=100)  
    createduser = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name="emp_crtdusr",blank=True, null=True)
    modifieduser = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name="emp_mdfddusr",blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    modified_datetime = models.DateTimeField(blank=True, null=True,auto_now=True)
    isbillable = models.BooleanField(db_column='isBillable' ,blank=True, null=True)
    project=models.ForeignKey(Project, on_delete=models.DO_NOTHING,related_name="empprojects")
    company=models.ForeignKey(Company, on_delete=models.DO_NOTHING,related_name="companyemp")
    class Meta:
        managed = False
        db_table = 'Employees'
        unique_together=["first_name","last_name"]


class EmployePasswords(models.Model):
    emp_password_id = models.AutoField(primary_key=True)
    # emp_id = models.IntegerField()
    emp=models.ForeignKey(Employees, on_delete=models.DO_NOTHING, related_name="emp_passwrd")
    password = models.CharField(max_length=200)
    createduser = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name="emppass_crtdusr",blank=True, null=True)
    modifieduser = models.ForeignKey(Users,on_delete=models.DO_NOTHING,related_name="emppass_mdfddusr",blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    modified_datetime = models.DateTimeField(blank=True, null=True,auto_now=True)

    class Meta:
        managed = False
        db_table = 'employe_passwords'
