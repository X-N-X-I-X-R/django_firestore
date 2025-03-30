from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .log import setup_logger

logger = setup_logger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal to handle user post-save operations.
    This is a backup mechanism in case the registration process fails.
    """
    if created:
        try:
            logger.info(f"New user created via signal: {instance.email}")
        except Exception as e:
            logger.error(f"Error in user_post_save signal for {instance.email}: {str(e)}") 