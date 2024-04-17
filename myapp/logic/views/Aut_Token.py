from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from termcolor import colored

from myapp.models import UserProfile

class AutenticacionToken(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        print(colored('Getting token for user: ' + user.username, 'green'))
        token = super().get_token(user)

        # Add custom claims
        token['is_staff'] = user.is_staff
        token['is_superuser'] = user.is_superuser
        token['is_active'] = user.is_active
        token['last_login'] = user.last_login.isoformat() if user.last_login else None
        token['id'] = user.id
        token['groups'] = [group.name for group in user.groups.all()]
        token['username'] = user.username
        token['email'] = user.email
        token['created_token_time'] = token['iat']
        token['time_to_expired'] = token['exp']

        if user.is_superuser:
            token['user_permissions'] = "The king, All permissions Allow"
        else:
            permissions = user.user_permissions.all()
            token['user_permissions'] = ', '.join(perm.codename for perm in permissions)
            print(colored('User permissions: ' + token['user_permissions'], 'green'))

        return token  # Removed the comma here
    
class AutenticacionTokenView(TokenObtainPairView):
    serializer_class = AutenticacionToken
    
class LogoutView(APIView):
    def post(self, request):
        refresh_token = request.data.get("refresh_token")

        if refresh_token is None:
            print(colored('Refresh token is required', 'red'))
            return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            print(colored('Invalid token', 'red'))
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        print(colored('Token blacklisted successfully', 'green'))
        return Response(status=status.HTTP_205_RESET_CONTENT)




