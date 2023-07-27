from datetime import datetime
from rest_framework import serializers, status

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from Account.mailer import send_email
from Account.models import Company, Project
from Account.serializers import CompanySerializer, ProjectSerializer
from Account.services import get_cached_user
from django.db import transaction

from Employee.models import EmployePasswords, Employees, Salary

class EmployePasswordsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=EmployePasswords
        fields="__all__"
        

class EmployeesSerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()
    company=CompanySerializer( read_only=True)
    project=ProjectSerializer( read_only=True)
    salary=serializers.SerializerMethodField()

    def get_createduser(self, obj):
        return get_cached_user(obj.createduser_id)

    def get_modifieduser(self, obj):
        return get_cached_user(obj.modifieduser_id)
    
    def get_salary(self,obj):
        sal_obj=Salary.objects.filter(emp=obj).order_by("-modifieddatetime").first()
        if sal_obj:
            serializer=EmpSalarySerializer(sal_obj)
            return serializer.data
        return None        
        
    
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
        validated_data['company']=Company.objects.get(pk=company)
        try:
            instance=super().create(validated_data)
            
            #TODO Email setup
            
            # need to entry into salary table
            salary=self.context["request"].data.get("salary",None)
            infra=self.context["request"].data.get("infracost",None)
            billtype=self.context["request"].data.get("isbillable",None)
            project=self.context["request"].data.get("project",None)
            if salary  and billtype is not None:
                sal_instance=Salary.objects.create(
                salary=salary,
                infracost=infra,
                isbillable=billtype,
                startdate=datetime.today(),
                createduser=user,
                modifieduser=user,
                createddatetime=datetime.now(),
                modifieddatetime=datetime.now(),
                emp=instance,
                project_id=project
                    
                )
            else:
                raise ValidationError({"Error":"Salary ,project and billing is required"})
            return instance
        except Exception as e:
                raise ValidationError( e)
            
    @transaction.atomic
    def update(self, instance, validated_data):
        from rest_framework.utils import model_meta
        info = model_meta.get_field_info(instance)
        """
        {
            "email":"ng@accentiqa.com",
            "password":"ng2020agroup"
        }
        
        """
        user=self.context["request"].user
        l_password = self.initial_data.get("password", None)
        m2m_fields = []
        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                m2m_fields.append((attr, value))
            else:
                setattr(instance, attr, value)
        setattr(instance,'modifieduser',user)
        setattr(instance,'modifieddatetime',datetime.now())
        try:
            instance.save()
            
            if instance.status==-1:
                if l_password is None:
                    raise ValidationError({"Error":"Password is required"})
            
            if l_password:
                emp_pass_qs=EmployePasswords.objects.filter(emp=instance).first()
                if emp_pass_qs:
                    emp_pass_qs.password=l_password
                    emp_pass_qs.createduser=user
                    emp_pass_qs.modifieduser=user
                    emp_pass_qs.save()
                else:
                    qs=EmployePasswords.objects.create(
                        emp=instance,
                        password=l_password,
                        createduser=user,
                        modifieduser=user
                    )
                    
            # Create or update salary table
            salary_obj = self.initial_data.get("salary", None)
            if salary_obj:
                salary_qs=Salary.objects.filter(emp=instance).order_by("-modifieddatetime").first()
                
                if salary_qs:
                    salary_dict={}
                    
                    salary_dict["createduser"]=user
                    salary_dict["modifieduser"]=user
                    salary_dict["createddatetime"]=datetime.now()
                    salary_dict["modifieddatetime"]=datetime.now()
                    salary_dict["startdate"]=datetime.today()
                    salary_dict["emp"]=instance
                    salary_dict["salary"]=salary_obj.get("salary", salary_qs.salary)
                    salary_dict["isbillable"]=salary_obj.get("isbillable", salary_qs.isbillable)
                    salary_dict["infracost"]=salary_obj.get("infracost", salary_qs.infracost)
                    salary_dict["project_id"]=salary_obj.get("project", salary_qs.project_id)
                    
                    Salary.objects.create(**salary_dict)
                    
                    salary_qs.enddate=datetime.today()
                    salary_qs.modifieddatetime=datetime.now()
                    salary_qs.modifieduser=user
                    salary_qs.save()
                    
            return instance
        except Exception as e:
            raise ValidationError(e)
                    


class EmpSalarySerializer(serializers.ModelSerializer):
        
    
    class Meta:
        model = Salary
        fields =  ['sal_id','salary','isbillable','infracost']        
class SalarySerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()
    def get_createduser(self, obj):
        return get_cached_user(obj.createduser_id)

    def get_modifieduser(self, obj):
        return get_cached_user(obj.modifieduser_id)
    
    class Meta:
        model = Salary
        fields =  "__all__"

        
class EmployeesalariesSerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()
    company=CompanySerializer( read_only=True)
    project=ProjectSerializer( read_only=True)
    salary=serializers.SerializerMethodField()

    def get_createduser(self, obj):
        return get_cached_user(obj.createduser_id)

    def get_modifieduser(self, obj):
        return get_cached_user(obj.modifieduser_id)
    
    def get_salary(self,obj):
        sal_obj=Salary.objects.filter(emp=obj).order_by("-modifieddatetime")
        if sal_obj:
            serializer=SalarySerializer(sal_obj,many=True)
            return serializer.data
        return None        
        
    
    class Meta:
        model = Employees
        fields = "__all__"