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
        validated_data['project']=Project.objects.get(pk=self.context["request"].data.get("project",None))
        validated_data['company']=Company.objects.get(pk=company)
        try:
            instance=super().create(validated_data)
            
            #TODO Email setup
            
            # need to entry into salary table
            salary=self.context["request"].data.get("salary",None)
            infra=self.context["request"].data.get("infracost",None)
            billtype=self.context["request"].data.get("isbillable",None)
            if salary  and billtype is not None:
                sal_instance=Salary.objects.create(
                salary=salary,
                infracost=infra,
                isbillable=billtype,
                startdate=datetime.today(),
                enddate=datetime.today(),
                createduser=user,
                modifieduser=user,
                createddatetime=datetime.now(),
                modifieddatetime=datetime.now(),
                emp=instance
                    
                )
            else:
                raise ValidationError({"Error":"Salary and billing is required"})
            return instance
        except Exception as e:
                raise ValidationError( e)
            
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
            
            sal_instance=Salary.objects.filter(emp=instance).order_by("-modifieddatetime")
            if self.initial_data.get("isbillable",None) is not None:
                sal_instance=sal_instance.filter(isbillable=self.initial_data.get("isbillable",None))
                if not sal_instance:
                    Salary.objects.create(
                        isbillable=self.initial_data.get("isbillable",None),
                        salary=self.initial_data.get("isbillable",sal_instance.salary),
                        infracost=self.initial_data.get('infracost',sal_instance.salary),
                        startdate=datetime.today(),
                        createduser_id=user,
                        modifieduser_id=user,
                        createddatetime=datetime.now(),
                        modifieddatetime=datetime.now(),
                        emp_id=instance
                        
                    )
                    sal_instance=sal_instance.first()
                    sal_instance.enddate=datetime.today()
                    sal_instance.save()
                else:
                    sal_instance=sal_instance.first()
                    Salary.objects.create(
                        isbillable=self.initial_data.get("isbillable",None),
                        salary=self.initial_data.get("salary",sal_instance.salary),
                        infracost=self.initial_data.get('infracost',sal_instance.infracost),
                        startdate=datetime.today(),
                        createduser=user,
                        modifieduser=user,
                        createddatetime=datetime.now(),
                        modifieddatetime=datetime.now(),
                        emp=instance
                    )
                    
                    sal_instance.enddate=datetime.today()
                    sal_instance.save()
            else:
                                
                salary=self.initial_data.get("salary",None)
                if salary:
                    Salary.objects.create(
                            isbillable=self.initial_data.get("isbillable",sal_instance.isbillable),
                            salary=self.initial_data.get("salary",sal_instance.salary),
                            infracost=self.initial_data.get('infracost',sal_instance.infracost),
                            startdate=datetime.today(),
                            createduser=user,
                            modifieduser=user,
                            createddatetime=datetime.now(),
                            modifieddatetime=datetime.now(),
                            emp=instance
                            
                        )
                    sal_obj=sal_instance.first()
                    sal_obj.enddate=datetime.today()
                    sal_obj.save()
                else:       
                
                    sal_instance=sal_instance.first()
                    sal_instance.infracost=self.initial_data.get("infracost", sal_instance.infracost)
                    sal_instance.save()
                
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