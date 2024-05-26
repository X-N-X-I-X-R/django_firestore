
# signals.py
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User

import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        logger.info(f'UserProfile created for user: {instance}')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()
    logger.info(f'UserProfile saved for user: {instance}')
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
    logger.info(f'ActivityLog created for {instance}')
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
  logger.info(f'ActivityLog deleted for {instance}')
  print('ActivityLog deleted message from --> receivers (signals.py)')    



