from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from django.utils import timezone
from decimal import Decimal
import uuid
import jwt
from datetime import datetime, timedelta
from django.utils.translation import gettext_lazy as _

class CoinManager(models.Manager):
    def create_coin(self, user, amount):
        """Create new coins for a user"""
        coin = self.create(
            user=user,
            amount=amount,
            code=str(uuid.uuid4()).replace('-', '')[:32]
        )
        return coin

    def generate_token(self, user_id, coin_type, amount):
        """Generate a unique JWT token for the coin"""
        payload = {
            'user_id': user_id,
            'coin_type': coin_type,
            'amount': str(amount),
            'created_at': datetime.utcnow().isoformat(),
            'exp': datetime.utcnow() + timedelta(days=365),  # Token valid for 1 year
            'token_id': str(uuid.uuid4())
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

    def verify_token(self, token):
        """Verify coin token and return payload"""
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

class Coin(models.Model):
    code = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coins')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_used = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    used_at = models.DateTimeField(null=True, blank=True)

    objects = CoinManager()

    def __str__(self):
        return f"{self.code} - {self.user.email}"

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = str(uuid.uuid4()).replace('-', '')[:32]
        super().save(*args, **kwargs)

class CoinTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('purchase', _('Purchase')),
        ('transfer', _('Transfer')),
        ('withdrawal', _('Withdrawal')),
        ('deposit', _('Deposit')),
        ('payment', _('Payment')),
        ('refund', _('Refund')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coin_transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.transaction_type} - {self.amount}"

class CoinPurchase(models.Model):
    STATUS_CHOICES = [
        ('pending', _('Pending')),
        ('completed', _('Completed')),
        ('failed', _('Failed')),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='coin_purchases')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} - {self.amount} coins - {self.status}"

    def save(self, *args, **kwargs):
        if self.status == 'completed' and not self.completed_at:
            self.completed_at = timezone.now()
        super().save(*args, **kwargs)

    def process_purchase(self):
        """Process the purchase and create coins"""
        if self.status != 'pending':
            return False, "Purchase already processed"

        try:
            # Create coins for the user
            coin = Coin.objects.create_coin(
                user=self.user,
                amount=self.amount
            )

            # Create transaction record
            CoinTransaction.objects.create(
                user=self.user,
                transaction_type='purchase',
                amount=self.amount,
                description=f'Purchase of {self.amount} coins'
            )

            self.status = 'completed'
            self.save()

            return True, "Purchase processed successfully"
        except Exception as e:
            self.status = 'failed'
            self.save()
            return False, str(e) 