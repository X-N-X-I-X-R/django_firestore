from rest_framework import serializers
from django_countries.fields import Country
from myapp.models.UserprofileFolder.userprofile_model import Images
from myapp.models.models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User




# serializers.py




class ImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'user_image_container', 'user_profile_image', 'image_subject']
        
class UserProfileSerializer(serializers.ModelSerializer):
    images = ImagesSerializer(many=True, read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            'user_nickname', 'user_gender', 'user_country',
            'user_birth_date', 'user_bio', 'user_website', 'active',
            'user_register_date', 'last_login', 'last_updated', 'id', 'images'
        ]

    def update(self, instance, validated_data):
        images_data = validated_data.pop('images', None)
        if images_data:
            for image_data in images_data:
                Images.objects.create(user=instance, **image_data)

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

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Images
        fields = ['user_image_container', 'user_profile_image']
