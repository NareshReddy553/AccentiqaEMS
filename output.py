# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


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


class UserPasswords(models.Model):
    user_password_id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    password = models.CharField(max_length=200, blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    created_user = models.IntegerField(blank=True, null=True)
    modified_user = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'User_Passwords'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    is_active = models.IntegerField()
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'


class EmployePasswords(models.Model):
    emp_password_id = models.IntegerField(primary_key=True)
    emp_id = models.IntegerField()
    password = models.CharField(max_length=200)
    created_user = models.IntegerField(blank=True, null=True)
    modified_user = models.IntegerField(blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employe_passwords'
