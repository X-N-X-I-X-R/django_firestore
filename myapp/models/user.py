from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator

class User(AbstractUser):
    """
    Base User model with essential fields
    """
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    password_confirmation = models.CharField(max_length=128)
    user_type = models.CharField(max_length=10, choices=[('advisor', 'Advisor'), ('customer', 'Customer')], default='customer')
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

class Customer(models.Model):
    """
    Customer model for regular users
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='customer')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

class AdvisorApplication(models.Model):
    """
    Model to handle advisor applications
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='advisor_application')
    professional_title = models.CharField(max_length=100)
    years_of_experience = models.PositiveIntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    specialization = models.CharField(max_length=200)
    education = models.TextField(validators=[MinLengthValidator(50)])
    certifications = models.TextField(blank=True)
    about = models.TextField(validators=[MinLengthValidator(100)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    admin_notes = models.TextField(blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Advisor Application - {self.user.email}"

    def approve(self):
        if self.status == 'pending':
            self.status = 'approved'
            self.processed_at = timezone.now()
            self.save()
            
            # Import here to avoid circular import
            from .advisor import Advisor
            
            # Create advisor profile
            Advisor.objects.create(
                user=self.user,
                name=f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username,
                description=self.about,
                experience=self.years_of_experience,
                professional_title=self.professional_title
            )
            # Update user type
            self.user.user_type = 'advisor'
            self.user.save()

    def reject(self, notes=''):
        if self.status == 'pending':
            self.status = 'rejected'
            self.admin_notes = notes
            self.processed_at = timezone.now()
            self.save()
