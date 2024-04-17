
#viewsets 
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import firebase_admin

from myapp.database.firestore import fire_db
from myapp.models.models import ActivityLog, Comment, Follow, Like, Message, Notification, Post, UserProfile
from myapp.logic.serializers import (
    ActivityLogSerializers, AutUser, CommentSerializers, FollowSerializers, 
    LikeSerializers, MessageSerializers, NotificationSerializers, 
    PostSerializers, RegisterSerializer, UserProfileSerializers)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site