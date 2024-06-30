# views_imports.py 
# pwd = /Users/elmaliahmac/Documents/Full_stack/Django_server/myapp/imports/views_imports.py


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
import logging
from myapp.models.UserprofileFolder.userprofile_model import Album, Images, UserProfile
from myapp.models.models import User, Post, Comment, Like, Follow, Notification, ActivityLog, Message, ActivateAccount_Email
from myapp.logic.convert_complex_data.serializers import (
    ActivityLogSerializer, AlbumSerializer, CommentSerializer, FollowSerializer, 
     LikeSerializer, MessageSerializer, NotificationSerializer, 
    UserProfileSerializer, RegisterSerializer, PostSerializer
)
from rest_framework_simplejwt.views import TokenRefreshView

from decouple import config
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.db.models import QuerySet
from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from typing import Type
from django.contrib.auth.models import User
from myapp.logic.convert_complex_data.serializers import UserProfileSerializer, RegisterSerializer
from myapp.logic.views.breacking_logic.activationEmail import send_activation_email


