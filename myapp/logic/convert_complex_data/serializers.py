from rest_framework import serializers
from myapp.models.UserprofileFolder.userprofile_model import Images
from myapp.models.models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User

class AutUser(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class UserProfileSerializer(serializers.ModelSerializer):
    user_country = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            'user_nickname', 'user_gender', 'user_country', 'user_phone', 
            'user_birth_date', 'user_bio', 'user_website', 'active', 
            'user_register_date', 'last_login', 'last_updated', 'id'
        ]

    def get_user_country(self, obj):
        return str(obj.user_country)


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'

class ActivityLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityLog
        fields = '__all__'

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['user_image_container', 'user_profile_image']
