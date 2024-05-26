
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User

# Signal to create a UserProfile instance whenever a new User instance is created
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    print('User created message from --> receivers (signals.py)')
    UserProfile.objects.create(user=instance)
    

# Signal to save the UserProfile instance whenever the related User instance is saved
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
  instance.userprofile.save()
  print('User saved message from --> receivers (signals.py)')
# Signal to create an ActivityLog instance whenever a new Post, Comment, Like, Follow, Notification, or Message instance is created
@receiver(post_save, sender=Post)
@receiver(post_save, sender=Comment)
@receiver(post_save, sender=Like)
@receiver(post_save, sender=Follow)
@receiver(post_save, sender=Notification)
@receiver(post_save, sender=Message)
def create_activity_log(sender, instance, created, **kwargs):
  if created:
    ActivityLog.objects.create(content_object=instance)
    print('ActivityLog created message from --> receivers (signals.py)')

# Signal to delete the ActivityLog instance whenever the related Post, Comment, Like, Follow, Notification, or Message instance is deleted
@receiver(pre_delete, sender=Post)
@receiver(pre_delete, sender=Comment)
@receiver(pre_delete, sender=Like)
@receiver(pre_delete, sender=Follow)
@receiver(pre_delete, sender=Notification)
@receiver(pre_delete, sender=Message)
def delete_activity_log(sender, instance, **kwargs):
  ActivityLog.objects.filter(content_object=instance).delete()
  print('ActivityLog deleted message from --> receivers (signals.py)')    


