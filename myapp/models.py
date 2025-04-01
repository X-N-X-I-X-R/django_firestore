from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from .models.user import User, Customer, Notification, Wallet, Transaction
from .models.advisor import (
    Advisor, Consultation, ServiceAvailability, VideoChat,
    PhoneCall, Order, Rating, Review, Follower, Subscription
)
from .models.coins import Coin, CoinTransaction, CoinPurchase

__all__ = [
    'User', 'Customer', 'Notification', 'Wallet', 'Transaction',
    'Advisor', 'Consultation', 'ServiceAvailability', 'VideoChat',
    'PhoneCall', 'Order', 'Rating', 'Review', 'Follower', 'Subscription',
    'Coin', 'CoinTransaction', 'CoinPurchase'   ,
]

class Transaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('999999.99'))
        ]
    )
    transaction_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Wallet(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class CoinTransaction(models.Model):
    wallet = models.ForeignKey('Wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('999999.99'))
        ]
    )
    transaction_type = models.CharField(max_length=20)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

class CoinPurchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('999999.99'))
        ]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('999999.99'))
        ]
    )
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class Order(models.Model):
    advisor = models.ForeignKey('Advisor', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(Decimal('0.01')),
            MaxValueValidator(Decimal('999999.99'))
        ]
    )
    status = models.CharField(max_length=20, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class Rating(models.Model):
    advisor = models.ForeignKey('Advisor', on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[
            MinValueValidator(Decimal('0.0')),
            MaxValueValidator(Decimal('5.0'))
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)

