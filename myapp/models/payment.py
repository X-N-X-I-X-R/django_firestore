from django.db import models
from django.conf import settings

class Payment(models.Model):
    """
    Payment model for handling all financial transactions
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='payments')
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50)  # e.g., 'credit_card', 'paypal', etc.
    transaction_id = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    platform_commission = models.DecimalField(max_digits=5, decimal_places=2, default=0.10)  # 10% by default
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    refunded_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.amount} ({self.status})"

    class Meta:
        ordering = ['-created_at'] 