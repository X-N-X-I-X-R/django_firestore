from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import (
    User, Customer, Notification, Wallet, Transaction,
    Advisor, Consultation, ServiceAvailability, VideoChat,
    PhoneCall, Order, Rating, Review, Follower, Subscription,
    Coin, CoinTransaction, CoinPurchase
)

User = get_user_model()

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'username', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'user__username')
    ordering = ('-created_at',)

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'title', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('recipient__email', 'title', 'message')
    ordering = ('-created_at',)

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__email',)
    ordering = ('-created_at',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('wallet', 'transaction_type', 'amount', 'status', 'created_at')
    list_filter = ('transaction_type', 'status', 'created_at')
    search_fields = ('wallet__user__email', 'description')
    ordering = ('-created_at',)

@admin.register(Advisor)
class AdvisorAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'slogan', 'rating', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__email', 'name', 'slogan', 'description')
    ordering = ('-created_at',)

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(ServiceAvailability)
class ServiceAvailabilityAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'day_of_week', 'start_time', 'end_time')
    list_filter = ('day_of_week', 'advisor')
    search_fields = ('advisor__name',)
    ordering = ('day_of_week', 'start_time')

@admin.register(VideoChat)
class VideoChatAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(PhoneCall)
class PhoneCallAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('advisor__name', 'customer__user__email', 'content')
    ordering = ('-created_at',)

@admin.register(Follower)
class FollowerAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('advisor', 'customer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('advisor__name', 'customer__user__email')
    ordering = ('-created_at',)

@admin.register(Coin)
class CoinAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'amount', 'is_used', 'created_at', 'used_at')
    list_filter = ('is_used', 'created_at', 'used_at')
    search_fields = ('user__email', 'code')
    ordering = ('-created_at',)

@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('user__email', 'description')
    ordering = ('-created_at',)

@admin.register(CoinPurchase)
class CoinPurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'price', 'status', 'created_at', 'completed_at')
    list_filter = ('status', 'created_at', 'completed_at')
    search_fields = ('user__email', 'transaction_id')
    ordering = ('-created_at',)

