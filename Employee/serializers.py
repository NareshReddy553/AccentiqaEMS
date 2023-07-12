from rest_framework import serializers

from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Employee.models import EmployePasswords, Employees

class EmployePasswordsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=EmployePasswords
        fields="__all__"
        

class EmployeesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Employees
        fields = "__all__"
        
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
        validated_data['createduser']=user
        validated_data['modifieduser']=user
        try:
            instance=super().create(validated_data)
            # TODO send email to admin for new emp approval
        except Exception as e:
                return e
    
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
            EmployePasswords.objects.create(
                emp=instance,
                password=l_password,
                createduser=user,
                updateduser=user
            )
            return instance
        except Exception as e:
            return e