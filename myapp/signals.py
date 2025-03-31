from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.conf import settings
from .models import Customer, User, Advisor, Wallet

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create user profile and wallet after user creation
    """
    if created:
        # Create wallet for all users
        Wallet.objects.create(user=instance)
        
        if instance.user_type == 'customer':
            Customer.objects.create(user=instance)
        elif instance.user_type == 'advisor' and not hasattr(instance, 'advisor'):
            # This case is handled by AdvisorApplication.approve()
            pass

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Signal to save user profile after user update
    """
    if instance.user_type == 'customer':
        if not hasattr(instance, 'customer'):
            Customer.objects.create(user=instance)
        instance.customer.save()
    elif instance.user_type == 'advisor':
        if hasattr(instance, 'advisor'):
            instance.advisor.save()

@receiver(pre_delete, sender=User)
def cleanup_user_data(sender, instance, **kwargs):
    """
    Clean up user related data before deletion
    """
    # Delete wallet
    if hasattr(instance, 'wallet'):
        instance.wallet.delete()
    
    # Delete profile based on user type
    if instance.user_type == 'advisor':
        if hasattr(instance, 'advisor'):
            instance.advisor.delete()
        if hasattr(instance, 'advisor_application'):
            instance.advisor_application.delete()
    elif instance.user_type == 'customer':
        if hasattr(instance, 'customer'):
            instance.customer.delete()
