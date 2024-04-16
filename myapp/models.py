
from myapp.imports import *


# validation for birth date 
def validate_birth_date(value):
    today = timezone.now().date()
    if value > today or value < today - relativedelta(years=18):
        raise ValidationError("Invalid birth date")

def default_date():
    return timezone.now().date() - relativedelta(years=18)

def validate_image_file_size(value):
    valid_types = ["image/png", "image/jpg", "image/jpeg", "image/gif", "image/bmp", "image/webp", "image/svg+xml", "image/tiff", "image/vnd.microsoft.icon", "image/vnd.wap.wbmp", "image/x-icon", "image/x-jng", "image/x-ms-bmp", "image/x-portable-bitmap", "image/x-xbitmap", "image/x-xpixmap", "image/x-xwindowdump"]
    
    if value.content_type not in valid_types:
        raise ValidationError("Unsupported file type")
    
    filesize = value.size
    
    if filesize < 4000000 or filesize > 7000000:  # 4MB to 7MB
        raise ValidationError("The file size must be between 4MB and 7MB")

def default_image():
    return "myapp/public/default.jpeg"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=25, editable=False)
    email = models.EmailField(editable=False)
    user_lastname = models.CharField(max_length=25)
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O')   
    user_country = models.CharField(max_length=25, default='United States')  
    user_phone = models.CharField(max_length=25, unique=True, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    user_birth_date = models.DateField(validators=[validate_birth_date], help_text="Enter your birth date in the format: YYYY-MM-DD", default=default_date)
    user_city = models.CharField(max_length=25)
    user_address = models.CharField(max_length=25, blank=True, null=True, help_text="Optional")    
    user_register_date = models.DateTimeField(auto_now_add=True,)
    last_login = models.DateTimeField(auto_now=True)
    user_image_container = models.ImageField(blank=True, null=True, validators=[validate_image_file_size])
    user_profile_image = models.ImageField(default=default_image, blank=True, null=True)
    
    def __str__(self):
        return self.username


 
        
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='posts')
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(750)],help_text= "The post must be between 1 and 500 characters long.",default="No content", blank=False, null=False)
    likes = models.ManyToManyField(UserProfile, related_name='liked_posts', blank=True)
    comments = models.ManyToManyField('Comment', related_name='post_comments', blank=True)
    image = models.ImageField(upload_to='posts/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_size])  
    created_at = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    tag_another_user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='tagged_posts', null=True, blank=True)
   
    def __str__(self):
        return f"{self.user.username}'s Post"

class Comment(models.Model):
    comments_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True) 
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) 
    replies = models.ManyToManyField('self', blank=True)  # Remove related_name attribute

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(validators=[MinLengthValidator(1), MaxLengthValidator(500)], help_text="The comment must be between 1 and 500 characters long.", default="No comment", blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def clean(self):
        if not self.parent_comment and self.replies.exists():
            raise ValidationError("You can't comment on an empty Comment.")
    
    def __str__(self):
        return f"{self.user.username}'s Comment"
    

class Like(models.Model):
    likes_id= models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username}'s Like"

class Follow(models.Model):
    follows_id= models.AutoField(primary_key=True)
    followee = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='followers')
    follower_user = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.follower_user.username} follows {self.followee.username}"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('tag', 'Tag'), 
        ('message', 'Message')
    ]
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='notifications')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}'s Notification"

class ActivityLog(models.Model):
    activity_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    action = models.CharField(max_length=50, choices=[('post', 'Post'), ('comment', 'Comment'), ('like', 'Like'), ('follow', 'Follow')])
    time = models.DateTimeField() 
    
    def __str__(self):
        return f"{self.user.username}'s Activity Log"

class Message(models.Model):
    message_id= models.AutoField(primary_key=True)
    sender = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def __str__(self):     
        return f"Message from {self.sender.username} to {self.recipient.username}"
    

