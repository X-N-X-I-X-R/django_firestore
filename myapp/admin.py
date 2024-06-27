from django.contrib import admin

# Register your models here.

from myapp.models.models import ActivityLog, Comment, Follow, Like, Message, Notification, Post, ActivateAccount_Email
from django.contrib.auth.models import User

from myapp.models.UserprofileFolder.userprofile_model import UserProfile




admin.site.register(ActivityLog)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Like)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(ActivateAccount_Email)







