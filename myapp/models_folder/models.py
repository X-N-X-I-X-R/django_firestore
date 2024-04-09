from django import db
from .imports  import  Group, Permission, models, _, MinValueValidator, MaxValueValidator,MinLengthValidator, MaxLengthValidator,RegexValidator,FileExtensionValidator,relativedelta,date, FileExtensionValidator, Image, GenericForeignKey, ContentType, ValidationError,timezone ,User,ValidationError,ValidationError

# validation for phone number
def validate_phone_number(value):
    if not value.startswith('+'):
        raise ValidationError("Phone number must start with a '+' sign")
    if not value[1:].isdigit():
        raise ValidationError("Phone number must contain only digits after the '+' sign")
    if len(value) < 9 or len(value) > 20:
        raise ValidationError("Phone number must be between 10 and 15 digits long")
    return value

# validation for birth date 
def validate_birth_date(value):
    today = timezone.now().date()
    if value > today or value < today - relativedelta(years=18):
        raise ValidationError("Invalid birth date")
    
    
from django.core.exceptions import ValidationError

def validate_image_file_size(value):
    filesize = value.size
    
    if filesize > 1048576:  # 1MB
        raise ValidationError("The maximum file size that can be uploaded is 1MB")
    else:
        return value    

# User model with personal details and access permissions to groups and specific user permissions
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=25, editable=False)
    email = models.EmailField(editable=False)
    user_lastname = models.CharField(max_length=25)
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='O')   
    user_country = models.CharField(max_length=25, default='United States')  
    user_phone = models.CharField(max_length=25, unique=True, validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])
    user_birth_date = models.DateField(default=timezone.now  , validators=[validate_birth_date])
    user_city = models.CharField(max_length=25)
    user_address = models.CharField(max_length=25, blank=True, null=True, help_text="Optional")    
    user_register_date = models.DateTimeField(auto_now_add=True,)
    last_login = models.DateTimeField(auto_now=True)
    user_imag_container = models.URLField(blank=True, null=True)
    user_profile_imag = models.URLField(blank=True, null=True)
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user    belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
        
    ) # check permissions&groups.py for the groups and permissions assignment  

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="%(app_label)s_%(class)s_related",
        related_query_name="%(app_label)s_%(class)ss",
    )
    

    def __str__(self):  
        return self.username
    
    def save(self, *args, **kwargs):
        print("Saving user profile")
        # If this is an existing instance (i.e., not a new user), and the user is not an admin
        if self.pk is not None and not self.user.is_superuser:
            # Get the old instance from the database
            old_instance = UserProfile.objects.get(pk=self.pk)  # No need to access the id attribute of the User object
            # If the groups or user_permissions have been changed
            if set(self.groups.all()) != set(old_instance.groups.all()) or \
               set(self.user_permissions.all()) != set(old_instance.user_permissions.all()):
                # Revert the changes
                self.groups.set(old_instance.groups.all())
                self.user_permissions.set(old_instance.user_permissions.all())
                # Optionally, raise a ValidationError to inform the user that they can't change their groups or permissions
                raise ValidationError("Non-admin users can't change their groups or permissions")

        self.username = self.user.username
        self.email = self.user.email
        super().save(*args, **kwargs)

 
        
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
    
