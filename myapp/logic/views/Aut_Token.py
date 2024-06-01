from typing import Type
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import Serializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from termcolor import colored
import json
import logging
import os
from myapp.models.models import User, ActivateAccount_Email, UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from ..convert_complex_data.serializers import RegisterSerializer, UserProfileSerializer, PostSerializer, CommentSerializers, LikeSerializers, FollowSerializers, NotificationSerializers, ActivityLogSerializers, MessageSerializers
from decouple import config


logger = logging.getLogger(__name__)

def send_activation_email(user, request):
    refresh = AutenticacionToken.get_token(user)
    refresh_token = str(refresh)
    current_site = get_current_site(request)
    mail_subject = 'Activate your account'
    message = render_to_string('acc_active_email.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        'refresh_token': refresh_token,
        'protocol': 'https' if request.is_secure() else 'http'
    })
    
    logger.debug("Attempting to send email to %s", user.email)
    try:
        email_host_user = config('EMAIL_HOST_USER')
        if not isinstance(email_host_user, str):
            raise ValueError("EMAIL_HOST_USER must be a string.")
        
        email = EmailMessage(
            mail_subject,
            message,
            email_host_user,
            [user.email],
        )
        email.content_subtype = "html"  # this is the crucial line
        email.send()
        logger.debug("Email sent to %s", user.email)
    except Exception as e:
        logger.error("Error sending email: %s", e)


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

        return token  
    
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

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()

    def get_serializer_class(self) -> Type[Serializer]:
        if self.action == 'register':
            return RegisterSerializer
        return UserProfileSerializer
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False  # Set the user as inactive until email verification
            )
        
          
            send_activation_email(user, request)
            return Response(RegisterSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(id=response.data['id'])  # type: ignore
        activation_email = ActivateAccount_Email(user=user)
        activation_email.generate_activation_key()
        activation_email.save()
        return response

class ActivateAccount(APIView):
    def get(self, request, uidb64=None, token=None):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            activation_email = ActivateAccount_Email.objects.get(user=user)
            activation_email.activate_account()
            activation_email.save()
            return redirect('http://localhost:4200/home/')
        else:
            return redirect('http://localhost:4200/market-data')


class UserProfileViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = UserProfile.objects.all()
        serializer = UserProfileSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile)
            return Response(serializer.data)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = UserProfileSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        try:
            user_profile = UserProfile.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def destroy(self, request, *args, **kwargs):
        try:
            user_profile = UserProfile.objects.get(pk=kwargs['pk'])
            user_profile.active = False
            user_profile.save()
            return Response({"message": "The profile has been removed."}, status=status.HTTP_200_OK)
        except UserProfile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializers

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers

class ActivityLogViewSet(viewsets.ModelViewSet):
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializers

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializers








# from rest_framework_simplejwt.views import TokenObtainPairView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework_simplejwt.exceptions import TokenError
# from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from termcolor import colored


# class AutenticacionToken(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         print(colored('Getting token for user: ' + user.username, 'green'))
#         token = super().get_token(user)

#         # Add custom claims
#         token['is_staff'] = user.is_staff
#         token['is_superuser'] = user.is_superuser
#         token['is_active'] = user.is_active
#         token['last_login'] = user.last_login.isoformat() if user.last_login else None
#         token['id'] = user.id
#         token['groups'] = [group.name for group in user.groups.all()]
#         token['username'] = user.username
#         token['email'] = user.email
#         token['created_token_time'] = token['iat']
#         token['time_to_expired'] = token['exp']

#         if user.is_superuser:
#             token['user_permissions'] = "The king, All permissions Allow"
#         else:
#             permissions = user.user_permissions.all()
#             token['user_permissions'] = ', '.join(perm.codename for perm in permissions)
#             print(colored('User permissions: ' + token['user_permissions'], 'green'))

#         return token  
    
# class AutenticacionTokenView(TokenObtainPairView):
#     serializer_class = AutenticacionToken
    
# class LogoutView(APIView):
#     def post(self, request):
#         refresh_token = request.data.get("refresh_token")

#         if refresh_token is None:
#             print(colored('Refresh token is required', 'red'))
#             return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             token = RefreshToken(refresh_token)
#             token.blacklist()
#         except TokenError:
#             print(colored('Invalid token', 'red'))
#             return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

#         print(colored('Token blacklisted successfully', 'green'))
#         return Response(status=status.HTTP_205_RESET_CONTENT)



# from django.contrib.auth.tokens import PasswordResetTokenGenerator

# class TokenGenerator(PasswordResetTokenGenerator):
#     def _make_hash_value(self, user, timestamp):
#         return (
#             str(user.pk) + str(timestamp) + str(user.is_active)
#         )

# account_activation_token = TokenGenerator()