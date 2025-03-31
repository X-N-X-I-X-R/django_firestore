from django.db import models
from django.conf import settings

class Notification(models.Model):
    """
    Unified notification model for both advisors and customers
    """
    TYPE_CHOICES = [
        ('consultation_request', 'Consultation Request'),
        ('consultation_confirmed', 'Consultation Confirmed'),
        ('consultation_cancelled', 'Consultation Cancelled'),
        ('payment_received', 'Payment Received'),
        ('review_received', 'Review Received'),
        ('coin_purchase', 'Coin Purchase'),
        ('coin_transfer', 'Coin Transfer'),
        ('withdrawal', 'Withdrawal'),
        ('deposit', 'Deposit'),
    ]

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} for {self.recipient.username}" 