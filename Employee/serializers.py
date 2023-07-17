from datetime import datetime
from rest_framework import serializers, status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from Account.mailer import send_email
from Account.models import Company, Project
from Account.serializers import CompanySerializer, ProjectSerializer
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
    company=CompanySerializer( read_only=True)
    project=ProjectSerializer( read_only=True)

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
            "first_name": "Nareqsh",
            "last_name": "Redqdy",
            "phone_number": 9398977891,
            "email": "Naresh.gqangireddy@accentiqa.com",
            "isbillable": 0,
            "project": 1,
            "company": 1
        }
        """
        company=self.context["request"].data.get("company",None)
        if not company:
            raise ValidationError({"error":"company is required in the payload"})
        user=self.context["request"].user
        validated_data["createduser"] = user
        validated_data["modifieduser"] = user
        validated_data['project']=Project.objects.get(pk=self.context["request"].data.get("project",None))
        validated_data['company']=Company.objects.get(pk=company)
        try:
            instance=super().create(validated_data)
            
            # context = {
            # }
            # x = datetime.now().strftime("%x %I:%M %p")
            # subject = f"TFN Recycle Request {x}"
            # send_email(
            #     template="index.html",
            #     subject=subject,
            #     context_data=context,
            #     recipient_list=['ngangireddy@accentiqa.com'],
            # )
            return instance
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
        if instance.status==-1:
            if l_password is None:
                raise ValidationError({"Error":"Password is required"})
        
        instance.email=validated_data.get('email', instance.email)
        instance.status=validated_data.get("status",instance.status)
        instance.isbillable=validated_data.get("isbillable",instance.isbillable)
        instance.project=validated_data.get("project",instance.project)
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