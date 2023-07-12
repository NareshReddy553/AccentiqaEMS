
from datetime import datetime
from typing import Any, Optional
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.base_user import AbstractBaseUser
from django.http.request import HttpRequest
from rest_framework_simplejwt.authentication import (
    AuthenticationFailed,
    InvalidToken,
    JWTAuthentication,
    api_settings,
)

from Account.models import UserPasswords, Users

class ModelBackend(BaseBackend):
    
    def authenticate(self, request, username, password, **kwargs) :
        
        try:
            user = Users.objects.get(
                username__iexact=username,
                is_active=True,
            )
        except Users.DoesNotExist:
            return None

        if user is None:
            return None

        # logger.debug("User ID: " + str(user.user_id))
        userPass = (
            UserPasswords.objects.filter(user=user).first()
        )

        # in case we don't need to populate a user's profile to django.contrib.auth.models.User, we can use following
        # simple query
        # userPass = UsersPasswords.objects.filter(user__username=username).order_by('-userpassword_id').first()

        if userPass is None:
            return None
        
        if not userPass.password==password:
            return None

        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")

       
        return user
    
class AccountJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))

        # use memory cache for better performance
        
        
        try:
            user = Users.objects.get(pk=user_id)
        except Users.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")

        
        if not user.is_active:
            raise AuthenticationFailed(_("User is inactive"), code="user_inactive")
        user.is_authenticated = True
        return user
