from rest_framework import serializers

from Account.models import Company, UserPasswords, Users,Project
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Account.services import get_cached_user


class CompanySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Company
        fields = "__all__"
        
class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = "__all__"
        
class UsersSerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()
    company=CompanySerializer(read_only=True)

    def get_createduser(self, obj):
        return get_cached_user(obj.createduser_id)

    def get_modifieduser(self, obj):
        return get_cached_user(obj.modifieduser_id)
    class Meta:
        model = Users
        fields = "__all__"

    def create(self, validated_data):
        """
        {
            "first_name":"naresh"
            "last_name":"reddy",
            "email":"nareshgangireddy@gmail.com",
            "password":"ng@123"
        }
        """
        company=self.context["request"].headers.get("company")
        user=self.context["request"].user
        validated_data['company']=company
        l_password = self.initial_data.get("password", None)
        if l_password is None:
            raise ValidationError({"Error":"Password is required"})
        instance=super().create(validated_data)
        UserPasswords.objects.create(
            user=user,
            password=l_password,
            createduser=user,
            modifieduser=user
        )
        
        return instance
    
