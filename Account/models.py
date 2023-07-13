from django.db import models
from django.utils.translation import gettext as _

# Create your models here.


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    username = models.CharField(unique=True, max_length=100)
    email = models.CharField(unique=True, max_length=100)
    is_active = models.IntegerField()
    created_datetime = models.DateTimeField(blank=True, null=True,auto_now_add=True)
    modified_datetime = models.DateTimeField(blank=True, null=True,auto_now=True)

    class Meta:
        managed = False
        db_table = 'Users'

class UserPasswords(models.Model):
    user_password_id = models.IntegerField(primary_key=True)
    user=models.ForeignKey(Users, on_delete=models.CASCADE,related_name="userpassword")
    password = models.CharField(max_length=200, blank=True, null=True)
    created_datetime = models.DateTimeField(blank=True, null=True)
    modified_datetime = models.DateTimeField(blank=True, null=True)
    # created_user = models.IntegerField(blank=True, null=True)
    createduser=models.ForeignKey(Users, on_delete=models.CASCADE,related_name="usrpswrd_crtusr")
    # modified_user = models.IntegerField(blank=True, null=True)
    modifieduser=models.ForeignKey(Users, on_delete=models.CASCADE,related_name="usrpswrd_mdfydusr")
     
    class Meta:
        managed = False
        db_table = 'User_Passwords'



        


