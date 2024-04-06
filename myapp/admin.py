from django.contrib import admin
from .models_folder.models import UserProfile, Post, Comment, Like, Follow

class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('last_login', 'last_name',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)