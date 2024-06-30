from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django_countries.fields import CountryField
from django.core.exceptions import ValidationError
import random

def default_date():
    return timezone.now().date() - relativedelta(years=18)

def validate_image_file_size(image):
    if hasattr(image, 'file') and hasattr(image.file, 'size'):
        file_size = image.file.size
    else:
        file_size = len(image.file.getvalue())
    limit_mb = 5
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError(_('User profile image must be less than %s MB.' % limit_mb))

def user_directory_path(instance, filename):
    if not filename:
        random_number = random.randint(1000, 9999)
        filename = f'random_{random_number}.jpg'
    else:
        filename = filename.replace(' ', '_')

    if hasattr(instance, 'userprofile') and instance.userprofile:
        user_id = instance.userprofile.user.id
    elif hasattr(instance, 'user') and instance.user:
        user_id = instance.user.id
    else:
        user_id = 'unknown'
    
    return f'user_{user_id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    user_nickname = models.CharField(max_length=25, blank=True, null=True)
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='', blank=True, null=True)
    user_country = CountryField(blank=True, null=True)
    user_birth_date = models.DateField(default=default_date, blank=True, null=True)
    user_register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)
    user_bio = models.TextField(blank=True, null=True)
    user_website = models.URLField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_private_or_global = models.BooleanField(default=False, blank=True, null=True,choices=[(True, 'Private'), (False, 'Global')])
    
    def get_user_id(self):
        return self.user.id # type: ignore

    def save(self, *args, **kwargs):
        if not self.user_nickname:
            self.user_nickname = self.user.username
        self.clean()
        if not self.last_login:
            self.last_login = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)

    def validate_nickname(self, nickname):
        if UserProfile.objects.filter(user_nickname=nickname).exists():
            raise ValidationError(_('User nickname must be unique.'))
        if nickname and len(nickname) < 3:
            raise ValidationError(_('User nickname must be at least 3 characters long.'))

    def validate_birth_date(self):
        if self.user_birth_date and self.user_birth_date > timezone.now().date():
            raise ValidationError(_('Birth date cannot be in the future.'))

    def validate_bio(self):
        if self.user_bio and len(self.user_bio) > 500:
            raise ValidationError(_('User bio must be less than 500 characters.'))

    def validation_models(self):
        self.validate_nickname(self.user_nickname)
        self.validate_birth_date()
        self.validate_bio()

    def __str__(self):
        return self.user.username

class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_private_or_global = models.BooleanField(default=False, blank=True, null=True,choices=[(True, 'Private'), (False, 'Global')])

    def get_album_id(self):
        return self.id # type: ignore
    
    def save(self, *args, **kwargs):
        self.clean()
        super(Album, self).save(*args, **kwargs)
        
    def validate_title(self):
        if Album.objects.filter(title=self.title).exists():
            raise ValidationError(_('Album title must be unique.'))
        if self.title and len(self.title) < 3:
            raise ValidationError(_('Album title must be at least 3 characters long.'))
        
    def validation_models(self):
        self.validate_title()
        
    def __str__(self):
        return self.title

class Images(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='images')
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='images')
    user_image_container = models.ImageField(
        upload_to=user_directory_path,
        validators=[validate_image_file_size]
    )
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    image_subject = models.CharField(max_length=25, blank=True, null=True)
    is_private_or_global = models.BooleanField(default=False, blank=True, null=True,choices=[(True, 'Private'), (False, 'Global')])
    is_profile_picture = models.BooleanField(default=False)
    
    def get_image_id(self):
        return self.id # type: ignore
    
    def save(self, *args, **kwargs):
        self.clean()
        super(Images, self).save(*args, **kwargs)
        
    def validate_image_subject(self):
        if Images.objects.filter(image_subject=self.image_subject).exists():
            raise ValidationError(_('Image subject must be unique.'))
        if self.image_subject and len(self.image_subject) < 3:
            raise ValidationError(_('Image subject must be at least 3 characters long.'))
        
    def validation_models(self):
        self.validate_image_subject()
        
    def __str__(self):
        return self.image_subject if self.image_subject else ''



