from rest_framework import serializers
from django_countries.fields import Country
from myapp.models.UserprofileFolder.userprofile_model import Album, Images
from myapp.models.models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User




# serializers.py




        
from rest_framework import serializers
from django_countries.fields import Country
from myapp.models.UserprofileFolder.userprofile_model import Album, Images
from myapp.models.models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User

# serializers.py

from rest_framework import serializers


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user', 'user_nickname', 'user_gender', 'user_country', 'user_birth_date', 'user_register_date', 'last_login', 'user_bio', 'user_website', 'active', 'last_updated', 'is_private_or_global']


    def update(self, instance, validated_data):
        country_data = validated_data.pop('user_country', None)
        if country_data:
            instance.user_country = Country(code=country_data['code'])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


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





class AlbumSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')  # Assuming you want to display the username of the user

    class Meta:
        model = Album
        fields = ['id', 'user', 'title', 'created_at', 'is_private_or_global']
        read_only_fields = ['id', 'user', 'created_at']


class ImageSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.user.username')
    album = AlbumSerializer(read_only=True)
    user_image_container = serializers.ImageField(use_url=True)

    class Meta:
        model = Images
        fields = ['id', 'user', 'album', 'user_image_container', 'created_at', 'image_subject', 'is_profile_picture', 'is_private_or_global']
        read_only_fields = ['id', 'user', 'created_at']
