from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
import re
from django_countries.fields import CountryField

def default_date():
    tiimezone = timezone.now().date() - relativedelta(years=18)
    return tiimezone
  
from django.templatetags.static import static

def default_image():
    return static('/Users/elmaliahmac/Documents/Full_stack/Django_server/media/default.jpeg')
    
def validate_image_file_size(image):
        file_size = image.file.size
        limit_mb = 5
        if file_size > limit_mb * 1024 * 1024:
            raise ValidationError(_('User profile image must be less than %s MB.' % limit_mb))
        

                                                 
                                                 
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)                
                                                 
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_nickname = models.CharField(max_length=25, blank=True, null=True)
    user_gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='', blank=True, null=True)
    user_country = CountryField(blank=True, null=True)
    user_phone = models.CharField(max_length=25, blank=True, null=True)
    user_birth_date = models.DateField(default=default_date, blank=True, null=True)
    user_register_date = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)  # הסר את auto_now
    user_bio = models.TextField(blank=True, null=True)
    user_website = models.URLField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)  # שדה חדש
    def get_user_id(self):
      user_Profile_id=self.user.id # type: ignore
      return user_Profile_id
    

    


    def __init__(self, *args, **kwargs):
        super(UserProfile, self).__init__(*args, **kwargs)
        self.__original_state = self.__dict__.copy()
        
    def save(self, *args, **kwargs):
        if not self.user_nickname:
            self.user_nickname = self.user.username
        self.clean()  # Call clean to validate before saving
        if not self.last_login:  # עדכן last_login רק אם הוא לא קיים
            self.last_login = timezone.now()
        super(UserProfile, self).save(*args, **kwargs)

 
    
    
    
    @staticmethod    
    def validate_nickname(nickname):
        # User Nickname Validation
        if UserProfile.objects.filter(user_nickname=nickname).exists():
            raise ValidationError(_('User nickname must be unique.'))
        # User Nickname Length Validation
        if nickname and len(nickname) < 3:
            raise ValidationError(_('User nickname must be at least 3 characters long.'))
  
    # def validate_phone(self):
    #   # User Phone Validation
    #   if self.user_phone and not re.match(r'^\+?1?\d{9,15}$', self.user_phone):
    #     raise ValidationError(_('Enter a valid phone number.'))

    def validate_birth_date(self):
      # User Birth Date Validation
      if self.user_birth_date and self.user_birth_date > timezone.now().date():
        raise ValidationError(_('Birth date cannot be in the future.'))

    def validate_bio(self):
      # User Bio Length Validation
      if self.user_bio and len(self.user_bio) > 500:
        raise ValidationError(_('User bio must be less than 500 characters.'))


    def validation_models(self):
        self.validate_nickname(self.user_nickname)
        self.validate_birth_date()
        self.validate_bio()
        
  

    def __str__(self):
        return self.user.username
      
      
      
class Images(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
    user_image_container = models.ImageField(default=default_image, blank=True, null=True,upload_to=user_directory_path)
    user_profile_image = models.ImageField(default=default_image, blank=True, null=True,upload_to=user_directory_path)
    
    def __init__(self, *args, **kwargs):  
        super(Images, self).__init__(*args, **kwargs)
        self.__original_state = self.__dict__.copy()  
        
    def save(self, *args, **kwargs):
      self.clean()
      if self.__dict__ != self.__original_state:
        super(Images, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.user.user.user_nickname # type: ignore
      
    


