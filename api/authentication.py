from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from account.models import User

# imports for second view
from datetime import datetime, timedelta
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token
from django.utils import timezone


class customAuthentication(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None




class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Token'

    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.get(key=key)
        except model.DoesNotExist:
            raise AuthenticationFailed('Invalid token')

        if not token.user.is_active:
            raise AuthenticationFailed('User inactive or deleted')

        # Check token expiry time
        time_elapsed = timezone.now() - token.created
        if time_elapsed > timedelta(minutes=1): # set token expiry time to 1 minute
            token.delete()
            raise AuthenticationFailed('Token has expired')

        return (token.user, token)