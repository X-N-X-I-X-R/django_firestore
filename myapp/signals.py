from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User)
def user_post_save(sender, instance, created, **kwargs):
    """
    Signal to handle user post-save operations
    """
    if created:
        logger.info(f"Attempting to send welcome email to {instance.email}")
        try:
            # Send welcome email
            send_mail(
                'Welcome to Our Platform',
                f'Hi {instance.username},\n\nWelcome to our platform! We are excited to have you on board.',
                settings.DEFAULT_FROM_EMAIL,
                [instance.email],
                fail_silently=False,  # Changed to False to see errors
            )
            logger.info(f"Successfully sent welcome email to {instance.email}")
        except Exception as e:
            logger.error(f"Failed to send welcome email to {instance.email}: {str(e)}") 