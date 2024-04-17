
#viewsets 
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
import firebase_admin

from myapp.firestore import fire_db
from myapp.models import ActivityLog, Comment, Follow, Like, Message, Notification, Post, UserProfile
from myapp.serializers import (
    ActivityLogSerializers, AutUser, CommentSerializers, FollowSerializers, 
    LikeSerializers, MessageSerializers, NotificationSerializers, 
    PostSerializers, RegisterSerializer, UserProfileSerializers)
from django.contrib.auth.models import User
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.sites.shortcuts import get_current_site





class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AutUser
    
    
class UserProfileViewSet(viewsets.ModelViewSet):
    """Viewset for the UserProfile model."""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializers

    @action(detail=False, methods=['get'], url_path='search')
    def search(self, request):
        query = request.query_params.get('query', '')
        users = UserProfile.objects.filter(user__username__icontains=query)
        serializer = UserProfileSerializers(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
        


class PostViewSet(viewsets.ModelViewSet):
    """Viewset for the Post model."""
    queryset = Post.objects.all()
    serializer_class = PostSerializers


class CommentViewSet(viewsets.ModelViewSet):
    """Viewset for the Comment model."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializers


class LikeViewSet(viewsets.ModelViewSet):
    """Viewset for the Like model."""
    queryset = Like.objects.all()
    serializer_class = LikeSerializers


class FollowViewSet(viewsets.ModelViewSet):
    """Viewset for the Follow model."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializers


class NotificationViewSet(viewsets.ModelViewSet):
    """Viewset for the Notification model."""
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializers


class ActivityLogViewSet(viewsets.ModelViewSet):
    """Viewset for the ActivityLog model."""
    queryset = ActivityLog.objects.all()
    serializer_class = ActivityLogSerializers


class MessageViewSet(viewsets.ModelViewSet):
    """Viewset for the Message model."""
    queryset = Message.objects.all()
    serializer_class = MessageSerializers
    
    





from firebase_admin import credentials, firestore, initialize_app, get_app

# Initialize Firebase Admin SDK and Firestore client once when your application starts
cred = credentials.Certificate("/Users/elmaliahmac/Documents/json_keys/serviceAccountKey.json")

try:
    default_app = get_app()
except ValueError as e:
    default_app = initialize_app(cred)

db = firestore.client()



# Viewset for user registration and email verification 
class RegisterViewSet(viewsets.GenericViewSet):
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create a new User instance
            user = User.objects.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password'],
                is_active=False  # User is not active until email is validated
            )
            # Save the User instance
            user.save()

            # Generate a token for the user
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh)

            # Generate a validation link
            current_site = get_current_site(request).domain
            relative_link = reverse('email-verify')
            abs_url = 'http://'+current_site+relative_link+"?token="+access_token

            # Send a validation email
            send_mail(
                'Verify your email',
                'Hi '+user.username+', use the link below to verify your email \n' + abs_url,
                'noreply@mywebsite.com',
                [user.email],
                fail_silently=False,
            )

            # Use the Firestore client
            try:
                fire_db(db)
            except ValueError as e:
                print(e)

            # Return a successful response with the created User instance
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            # If the data is not valid, return a 400 Bad Request response with the validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)