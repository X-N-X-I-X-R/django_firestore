from django.contrib import admin

from myapp.models.models import Follow, Like, Post, UserProfile , Comment

class UserProfileAdmin(admin.ModelAdmin):
    exclude = ('last_login', 'last_name',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)