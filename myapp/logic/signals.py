from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from myapp.models.models import ActivateAccount_Email, UserProfile, Post, Comment, Like, Follow, Notification, ActivityLog, Message
from django.contrib.auth.models import User
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=User)
def create_activation_email(sender, instance, created, **kwargs):
    if created:
        ActivateAccount_Email.objects.create(user=instance)
        
        logger.info(f'ActivateAccount_Email created for user: {instance}')

@receiver(post_save, sender=ActivateAccount_Email)
def create_user_profile(sender, instance, **kwargs):
    if instance.is_active:
        UserProfile.objects.create(user=instance.user)
        logger.info(f'UserProfile created for user: {instance.user}')

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
        logger.info(f'UserProfile saved for user: {instance}')
    except UserProfile.DoesNotExist:
        pass

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

@receiver(pre_delete, sender=Post)
@receiver(pre_delete, sender=Comment)
@receiver(pre_delete, sender=Like)
@receiver(pre_delete, sender=Follow)
@receiver(pre_delete, sender=Notification)
@receiver(pre_delete, sender=Message)
def delete_activity_log(sender, instance, **kwargs):
    ActivityLog.objects.filter(content_object=instance).delete()
   
    logger.info(f'ActivityLog deleted for {instance}')



def messege():
  if create_activation_email or create_user_profile or save_user_profile or create_activity_log or delete_activity_log:
    return "signals.py file is working"
  else:
    pass

messege()