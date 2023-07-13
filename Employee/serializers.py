from rest_framework import serializers, status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from Account.services import get_cached_user
from django.db import transaction

from Employee.models import EmployePasswords, Employees

class EmployePasswordsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=EmployePasswords
        fields="__all__"
        

class EmployeesSerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()

    def get_createduser(self, obj):
        return get_cached_user(obj.createduser_id)

    def get_modifieduser(self, obj):
        return get_cached_user(obj.modifieduser_id)
    
    class Meta:
        model = Employees
        fields = "__all__"
        
    @transaction.atomic    
    def create(self, validated_data):
        """
        {
            "first_name":"Naresh",
            "last_name":"Reddy",
            "phone_number":9398977891,
            "email:"Naresh.gangireddy@accentiqa.com"
        }
        """
        user=self.context["request"].user
        validated_data["createduser"] = user
        validated_data["modifieduser"] = user
        try:
            instance=super().create(validated_data)
            return instance
            # TODO send email to admin for new emp approval
        except Exception as e:
                return e
            
    @transaction.atomic
    def update(self, instance, validated_data):
        
        """
        {
            "email":"ng@accentiqa.com",
            "password":"ng2020agroup"
        }
        
        """
        user=self.context["request"].user
        l_password = self.initial_data.get("password", None)
        if l_password is None:
            raise ValidationError({"Error":"Password is required"})
        
        instance.email=validated_data.get('email', instance.email)
        try:
            instance.save()
            # update the password
            emp_pass_qa=EmployePasswords.objects.filter(emp=instance).first()
            if emp_pass_qa:
                emp_pass_qa.password=l_password
                emp_pass_qa.createduser=user
                emp_pass_qa.modifieduser=user
                emp_pass_qa.save()
            else:
                qs=EmployePasswords.objects.create(
                    emp=instance,
                    password=l_password,
                    createduser=user,
                    modifieduser=user
                )
            return instance
        except Exception as e:
            return e