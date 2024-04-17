from django.forms import ValidationError
from rest_framework import serializers
from myapp.models.models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User 


class AutUser(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = '__all__'
    
class UserProfileSerializers(serializers.ModelSerializer):
  class Meta:
    model = UserProfile
    fields = '__all__'

class PostSerializers(serializers.ModelSerializer):
  class Meta:
    model = Post
    fields = '__all__'

class CommentSerializers(serializers.ModelSerializer):
  class Meta:
    model = Comment
    fields = '__all__'

class LikeSerializers(serializers.ModelSerializer):
  class Meta:
    model = Like
    fields = '__all__'

class FollowSerializers(serializers.ModelSerializer):
  class Meta:
    model = Follow
    fields = '__all__'

class NotificationSerializers(serializers.ModelSerializer):
  class Meta:
    model = Notification
    fields = '__all__'

class ActivityLogSerializers(serializers.ModelSerializer):
  class Meta:
    model = ActivityLog
    fields = '__all__'

class MessageSerializers(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'
    


      
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        
