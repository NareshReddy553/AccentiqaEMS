from rest_framework import serializers

from Account.models import UserPasswords, Users
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from Account.services import get_cached_user


class UsersSerializer(serializers.ModelSerializer):
    createduser = serializers.SerializerMethodField()
    modifieduser = serializers.SerializerMethodField()

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
        user=self.context["request"].user
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