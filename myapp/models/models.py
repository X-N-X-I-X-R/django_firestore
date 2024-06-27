import re
import jwt
from yaml import serialize
from myapp.imports.model_imports import *
from .UserprofileFolder.userprofile_model import UserProfile
from django.db import models
import logging
from datetime import datetime, timedelta, timezone

logger = logging.getLogger(__name__)

class ActivateAccount_Email(models.Model):
    activation_id = models.AutoField(primary_key=True, help_text="The ID of the activation email.")
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)  # הוספת unique
    activation_key = models.CharField(max_length=40, help_text="The activation key for the account.")
    activation_date = models.DateTimeField(auto_now_add=True, help_text="The date when the activation email was sent.")
    is_active = models.BooleanField(default=False, help_text="Check this if the account has been activated.")
    
    def generate_activation_key(self):
        payload = {
            'exp': datetime.now(timezone.utc) + timedelta(days=2, seconds=3600),
            'iat': datetime.now(timezone.utc),
            'sub': self.user.id  # type: ignore
        }
        self.activation_key = jwt.encode(
            payload,
            'SECRET_KEY',  # Replace with your SECRET_KEY
            algorithm='HS256'
        )
        self.save()
        
    def activate_account(self):
        self.is_active = True
        logging.info(f"Account activated for {self.user.username}")
        return self.is_active
    
    def get_activation_key(self):
        logging.info(f"Activation key retrieved for user {self.user.username}")
        return self.activation_key  
    
    def __str__(self):
        return f"{self.user.username}'s Activation Email"

class Post(models.Model):
    post_id = models.AutoField(primary_key=True, help_text="The ID of the post.") 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts', help_text="Select the user who made the post.") 
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(750)], help_text= "The post must be between 1 and 750 characters long.", default="No content", blank=False, null=False) 
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True, help_text="Select the users who liked the post.") 
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True, help_text="Select the comments on the post.") 
    image = models.ImageField(upload_to='posts/', null=True, blank=True,  help_text="Upload an image for the post.")   
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the post was created.") 
    is_private = models.BooleanField(default=False, help_text="Check this if you want the post to be private.") 
    tagged_users = models.ManyToManyField(UserProfile, related_name='tagged_posts', blank=True, help_text="Select the users who are tagged in the post.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tagged_users.clear()
        self.add_tags()

    def add_tags(self):
        tagged_nicknames = re.findall(r'@(\w+)', self.content)
        tagged_users = UserProfile.objects.filter(user_nickname__in=tagged_nicknames)
        self.tagged_users.add(*tagged_users)
   
    def __str__(self):
        return f"{self.user.user_nickname}'s Post"

class Comment(models.Model): 
    comments_id = models.AutoField(primary_key=True, help_text="The ID of the comment.")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, help_text="Select the post that the comment is for.") 
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, help_text="Select the parent comment if this is a reply.") 
    replies = models.ManyToManyField('self', blank=True, help_text="Select the replies to this comment.")  
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments', help_text="Select the user who made the comment.")
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(500)], help_text="The comment must be between 1 and 500 characters long.", default="No comment", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the comment was created.")
    tagged_users = models.ManyToManyField(UserProfile, related_name='tagged_comments', blank=True, help_text="Select the users who are tagged in the comment.")  

    def clean(self):
        if self.parent_comment is None and self.replies.exists():
            raise ValidationError("You can't reply to an empty Comment.", code='invalid')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tagged_users.clear()
        self.add_tags()

    def add_tags(self):
        tagged_nicknames = re.findall(r'@(\w+)', self.content)
        tagged_users = UserProfile.objects.filter(user_nickname__in=tagged_nicknames)
        self.tagged_users.add(*tagged_users)
   
    def __str__(self):
        return f"{self.user.user_nickname}'s Comment"

class Like(models.Model): 
    likes_id= models.AutoField(primary_key=True, help_text="The ID of the like.")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, help_text="Select the user who made the like.")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, help_text="Select the content type of the liked object.")
    object_id = models.PositiveIntegerField(help_text="Enter the ID of the liked object.")
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the like was created.")

    class Meta:
        unique_together = ('user', 'content_type', 'object_id')

    def __str__(self):
        return f"{self.user.user_nickname}'s Like"

class Follow(models.Model):
    follows_id= models.AutoField(primary_key=True, help_text="The ID of the follow.")
    followerss = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers', help_text="Select the user who is being followed.")
    follower_user = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE, help_text="Select the user who is following.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the follow was created.")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['followerss', 'follower_user'], name='unique_follow')
        ]

    def __str__(self):
        return f"{self.follower_user.user.username} follows {self.followerss.user.username}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('tag', 'Tag'), 
        ('message', 'Message')
    ]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, help_text="Select the type of the notification.")
    notification_id = models.AutoField(primary_key=True, help_text="The ID of the notification.")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications', help_text="Select the user who will receive the notification.")
    content = models.TextField(help_text="Enter the content of the notification.", default="No content")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the notification was created.")
    is_read = models.BooleanField(default=False, help_text="Check this if the notification has been read.")

    def __str__(self):
        return f"{self.user.user_nickname}'s Notification"

class ActivityLog(models.Model):
    activity_id = models.AutoField(primary_key=True, help_text="The ID of the activity.")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, help_text="Select the user who performed the activity.")
    action = models.CharField(max_length=50, choices=[('post', 'Post'), ('comment', 'Comment'), ('like', 'Like'), ('follow', 'Follow')], help_text="Select the type of the activity.")
    time = models.DateTimeField(help_text="Enter the time when the activity was performed.") 

    def __str__(self):
        return f"{self.user.user_nickname}'s Activity Log"

class Message(models.Model):
    message_id= models.AutoField(primary_key=True, help_text="The ID of the message.")
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages', help_text="Select the user who sent the message.")
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages', help_text="Select the user who will receive the message.")
    content = models.TextField(help_text="Enter the content of the message.", default="No content")
    sent_at = models.DateTimeField(auto_now_add=True, help_text="The date when the message was sent.")
    is_read = models.BooleanField(default=False, help_text="Check this if the message has been read.")

    def __str__(self):     
        return f"Message from {self.sender.user.username} to {self.recipient.user.username}"
