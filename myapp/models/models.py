

import re
from myapp.imports.model_imports import *
from .models_Validations import *

    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, help_text="Select the user.")
    user_nickname = models.CharField(max_length=25, validators=[MinLengthValidator(1), MaxLengthValidator(25)], 
                                     help_text="The nickname must be between 1 and 25 characters long.", 
                                     blank=False, null=False, unique=True, 
                                     error_messages={'unique': 'A user with this nickname already exists.'}) 
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O', help_text="Select your gender.")   
    user_country = models.CharField(max_length=3 , choices=[(code, code) for code in validate_country()], default='USA', help_text="Select your country.")
    user_phone = models.CharField(max_length=25, unique=True, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")], help_text="Enter your phone number.", error_messages={'unique': 'A user with this phone number already exists.'}) 
    user_birth_date = models.DateField(validators=[validate_birth_date], help_text="Enter your birth date in the format: YYYY-MM-DD", default=default_date, blank=False, null=False) 
    user_register_date = models.DateTimeField(auto_now_add=True, help_text="The date when the user registered.") 
    last_login = models.DateTimeField(auto_now=True, help_text="The last login date.") 
    user_bio = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(500)], help_text="The bio must be between 1 and 500 characters long.", default="No bio", blank=False, null=False) 
    user_website = models.URLField(max_length=200, blank=True, null=True, default="No website added", help_text="Enter your website URL.") 
    user_image_container = models.ImageField(blank=True, null=True, validators=[validate_image_file_size], help_text="Upload your image.") 
    user_profile_image = models.ImageField(default=default_image, blank=True, null=True, help_text="Upload your profile image.") 

    def __str__(self):
        return self.user_nickname

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Call the "real" save() method.

 
        
class Post(models.Model):
    post_id = models.AutoField(primary_key=True, help_text="The ID of the post.") 
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts', help_text="Select the user who made the post.") 
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(750)], help_text= "The post must be between 1 and 750 characters long.", default="No content", blank=False, null=False) 
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True, help_text="Select the users who liked the post.") 
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True, help_text="Select the comments on the post.") 
    image = models.ImageField(upload_to='posts/', null=True, blank=True, validators=[validate_image_file_size], help_text="Upload an image for the post.")   
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the post was created.") 
    is_private = models.BooleanField(default=False, help_text="Check this if you want the post to be private.") 
    tagged_users = models.ManyToManyField(UserProfile, related_name='tagged_posts', blank=True, help_text="Select the users who are tagged in the post.")

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.tagged_users.clear()
        self.add_tags()

    def add_tags(self):
        # Extract the tagged nicknames from the post content.
        tagged_nicknames = re.findall(r'@(\w+)', self.content)

        # Get the UserProfile instances for the tagged nicknames.
        tagged_users = UserProfile.objects.filter(user_nickname__in=tagged_nicknames)

        # Add the tagged users to the post.
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
        # Extract the tagged nicknames from the post content.
        tagged_nicknames = re.findall(r'@(\w+)', self.content)

        # Get the UserProfile instances for the tagged nicknames.
        tagged_users = UserProfile.objects.filter(user_nickname__in=tagged_nicknames)

        # Add the tagged users to the post.
        self.tagged_users.add(*tagged_users)
   
    def __str__(self):
        return f"{self.user.user_nickname}'s Post"
    

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
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers', help_text="Select the user who is being followed.")
    follower_user = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE, help_text="Select the user who is following.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="The date when the follow was created.")

    def __str__(self):
        return f"{self.follower_user.user.username} follows {self.followee.user.username}"

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

'''

Here's what each `related_name` does:

1. `related_name='posts'` in `user` field: This allows you to access all posts of a user by using `user.posts.all()` where `user` is an instance of `UserProfile`.

2. `related_name='liked_posts'` in `likes` field: This allows you to access all posts liked by a user by using `user.liked_posts.all()` where `user` is an instance of `UserProfile`.

3. `related_name='post_comments'` in `comments` field: This allows you to access all posts a comment is associated with by using `comment.post_comments.all()` where `comment` is an instance of `Comment`.

4. `related_name='tagged_posts'` in `tag_another_user` field: This allows you to access all posts where a user is tagged by using `user.tagged_posts.all()` where `user` is an instance of `UserProfile`.

Without the `related_name` option, Django would use the lower-case name of the model, followed by `_set` (e.g., `post_set`) for the reverse relation. The `related_name` option allows you to set a custom name for this reverse relation.




#
In Django, if you need to create a relationship on a model that has not yet been defined, you can use the name of the model, rather than the model object itself. This is what you're doing with 'Comment'.
'''

'''

    The line likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True) in your Post model creates a many-to-many relationship between the Post and UserProfile models.
    This means that each Post can be liked by many UserProfile instances (users), and each UserProfile can like many Post instances.
    The blank=True option means that a Post can be created without any likes.
    The related_name='liked_posts' option allows you to access all posts liked by a user.


'''