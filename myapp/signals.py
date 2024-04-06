from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from .models_folder.models import Notification, UserProfile, Post, Comment, Like, Follow, ActivityLog, Message
from django.core.mail import send_mail
from django.utils import timezone, dateformat

def create_activity_log(user, action):
  formatted_time = dateformat.format(timezone.now(), 'Y-m-d H:i:s')
  ActivityLog.objects.create(user=user, action=action, time=formatted_time)

@receiver(post_save, sender=UserProfile)
def create_user_profile(sender, instance, created, **kwargs):
  if created:
    
    UserProfile.objects.create(user=instance)

@receiver(post_save, sender=UserProfile)
def save_user_profile(sender, instance, **kwargs):
  instance.profile.save()

@receiver(post_save, sender=Post)
def handle_post_save(sender, instance, created, **kwargs):
  action = 'created' if created else 'updated'
  create_activity_log(instance.user, f'{action} a post')

@receiver(post_save, sender=Comment)
def handle_comment_save(sender, instance, created, **kwargs):
  action = 'created' if created else 'updated'
  create_activity_log(instance.user, f'{action} a comment')

@receiver(post_save, sender=Like)
def handle_like_save(sender, instance, created, **kwargs):
  action = 'created' if created else 'updated'
  create_activity_log(instance.user, f'{action} a like')
  if created:
    Notification.objects.create(user=instance.content_object.user, content=f'{instance.user.username} liked your post', time=timezone.now())
    
@receiver(post_save, sender=Follow)
def handle_follow_save(sender, instance, created, **kwargs):
  action = 'started following' if created else 'updated follow'
  create_activity_log(instance.follower, f'{action} {instance.user.username}')
  if created:
    Notification.objects.create(user=instance.user, content=f'{instance.follower.username} started following you', time=timezone.now())


@receiver(post_save, sender=Message)
def handle_message_save(sender, instance, created, **kwargs):
  if created:
    Notification.objects.create(user=instance.recipient, content=f"You have a new message from {instance.sender.username}", time=timezone.now())
  else:
    create_activity_log(instance.sender, f"updated a message to {instance.recipient.username}")

@receiver(post_save, sender=Comment)
def comment_into_comment(sender, instance, created, **kwargs):
  if created and instance.parent_comment:
    instance.parent_comment.child_comments.add(instance)

@receiver([post_save, post_delete])
def create_activity_log(sender, instance, created=False, **kwargs):
  if sender not in [ActivityLog, Notification, UserProfile, Post, Comment, Like, Follow]:
    action = 'deleted' if not created else 'created' if created else 'updated'
    user = getattr(instance, 'user', None)
    if user is not None:
      create_activity_log(user, f'{action} a {sender.__name__.lower()}')

@receiver(pre_save, sender=UserProfile)
def handle_user_profile_image_update(sender, instance, **kwargs):
  if instance.pk:
    old_instance = UserProfile.objects.get(pk=instance.pk)
    if old_instance.user_profile_imag != instance.user_profile_imag:
      create_activity_log(instance, 'updated profile image')

@receiver(pre_save, sender=Post)
def handle_post_image_update(sender, instance, **kwargs):
  if instance.pk:
    old_instance = Post.objects.get(pk=instance.pk)
    if old_instance.image != instance.image:
      create_activity_log(instance.user, 'updated post image')

@receiver(post_save, sender=Post)
def handle_user_tag(sender, instance, created, **kwargs):
  if created and instance.tag_another_user:
    Notification.objects.create(user=instance.tag_another_user, content=f'{instance.user.username} tagged you in a post', time=timezone.now())

@receiver(post_save, sender=UserProfile)
def send_welcome_email(sender, instance, created, **kwargs):
  if created:
    try:
      send_mail(
        'Welcome to our site',
        'We are glad to have you here.',
        'from@example.com',
        [instance.email],
        fail_silently=False,
      )
    except Exception as e:
      print(f"Failed to send email due to {e}")
      
      
# dont forget to import the signals in the apps.py file  
# # explantion about signals  
  
# Signals are used to allow decoupled applications to get notified when certain actions occur elsewhere in the application. In a nutshell, signals allow certain senders to notify a set of receivers when some action has taken place. Theyre especially useful when many pieces of code may be interested in the same events.

# In this case, the signals are used to create a user profile when a user is created. The create_user_profile function creates a user profile when a user is created, and the save_user_profile function saves the user profile when the user is saved.

# The @receiver decorator is used to connect the signals to the functions. The post_save signal is sent when an object is saved, and the sender argument specifies the model that sends the signal. In this case, the post_save signal is sent when a UserProfile object is saved, and the sender argument specifies the UserProfile model.

# The create_user_profile function creates a user profile when a user is created. The UserProfile.objects.create(user=instance) line creates a user profile with the user field set to the user instance.

# The save_user_profile function saves the user profile when the user is saved. The instance.profile.save() line saves the user profile.

# The signals are connected to the UserProfile model using the @receiver decorator. The post_save signal is sent when a UserProfile object is saved, and the sender argument specifies the UserProfile model.

  

