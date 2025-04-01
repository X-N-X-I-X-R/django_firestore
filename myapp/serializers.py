from rest_framework import serializers
from django.contrib.auth import get_user_model
from decimal import Decimal
from .models import (
    User, Customer, Notification, Wallet, Transaction,
    Advisor, Consultation, ServiceAvailability, VideoChat,
    PhoneCall, Order, Rating, Review, Follower, Subscription,
    Coin, CoinTransaction, CoinPurchase, Payment, AdvisorApplication
)

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=[('advisor', 'Advisor'), ('customer', 'Customer')], required=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'password_confirmation',
                 'first_name', 'last_name', 'is_active', 'is_verified', 'user_type')
        read_only_fields = ('id', 'is_active', 'is_verified')

    def validate(self, data):
        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match'})
        
        # Add validation for advisor registration
        if data.get('user_type') == 'advisor':
            raise serializers.ValidationError({
                'user_type': 'Advisor registration is not allowed through regular registration. Please contact support.'
            })
        
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirmation')
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AdvisorApplicationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    password_confirmation = serializers.CharField(write_only=True)
    username = serializers.CharField(write_only=True)
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)

    class Meta:
        model = AdvisorApplication
        fields = (
            'id', 'email', 'username', 'password', 'password_confirmation',
            'first_name', 'last_name', 'professional_title', 'years_of_experience',
            'specialization', 'education', 'certifications', 'about', 'status',
            'submitted_at', 'processed_at'
        )
        read_only_fields = ('id', 'status', 'submitted_at', 'processed_at')

    def validate(self, data):
        if data.get('password') != data.get('password_confirmation'):
            raise serializers.ValidationError({'password_confirmation': 'Passwords do not match'})
        return data

    def create(self, validated_data):
        user_data = {
            'email': validated_data.pop('email'),
            'username': validated_data.pop('username'),
            'password': validated_data.pop('password'),
            'first_name': validated_data.pop('first_name'),
            'last_name': validated_data.pop('last_name'),
            'user_type': 'customer'  # Initially set as customer until approved
        }
        validated_data.pop('password_confirmation')
        
        # Create user
        user = User.objects.create_user(**user_data)
        
        # Create advisor application
        advisor_application = AdvisorApplication.objects.create(user=user, **validated_data)
        return advisor_application

# Base Serializers
class BaseUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active',)
        read_only_fields = ('id', 'is_active',)

class BaseCustomerSerializer(serializers.ModelSerializer):
    user = BaseUserSerializer(read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'user', 'is_active',)
        read_only_fields = ('id',)

class BaseNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('id', 'notification_type', 'title', 'message', 'is_read', 'created_at',)
        read_only_fields = ('id', 'created_at',)

class BaseWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('id', 'balance', 'created_at', 'updated_at',)
        read_only_fields = ('id', 'created_at', 'updated_at',)

class BaseTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id', 'transaction_type', 'amount', 'description', 'created_at',)
        read_only_fields = ('id', 'created_at',)

class BaseCoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        fields = ('id', 'code', 'amount', 'is_used', 'created_at', 'used_at',)
        read_only_fields = ('id', 'code', 'created_at', 'used_at',)

class BaseCoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransaction
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at',)
        read_only_fields = ('id', 'created_at',)

class BaseCoinPurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinPurchase
        fields = ('id', 'amount', 'price', 'status', 'transaction_id', 'created_at', 'completed_at',)
        read_only_fields = ('id', 'status', 'created_at', 'completed_at',)

    def validate(self, data):
        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError({'amount': 'Amount must be greater than 0'})
        if data.get('price', 0) <= 0:
            raise serializers.ValidationError({'price': 'Price must be greater than 0'})
        return data

# Customer Serializers
class CustomerSerializer(BaseCustomerSerializer):
    class Meta(BaseCustomerSerializer.Meta):
        fields = ('id', 'user', 'is_active', 'created_at', 'updated_at')
        read_only_fields = ('id', 'created_at', 'updated_at')

class CustomerUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active',)

class CustomerNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta):
        fields = ('id', 'notification_type', 'title', 'message', 'is_read', 'created_at',)

class CustomerWalletSerializer(BaseWalletSerializer):
    class Meta(BaseWalletSerializer.Meta):
        fields = ('id', 'balance', 'created_at', 'updated_at',)

class CustomerTransactionSerializer(BaseTransactionSerializer):
    class Meta(BaseTransactionSerializer.Meta):
        fields = ('id', 'transaction_type', 'amount', 'description', 'created_at',)

class CustomerCoinSerializer(BaseCoinSerializer):
    class Meta(BaseCoinSerializer.Meta):
        fields = ('id', 'amount', 'is_used', 'created_at',)

class CustomerCoinTransactionSerializer(BaseCoinTransactionSerializer):
    class Meta(BaseCoinTransactionSerializer.Meta):
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at',)

class CustomerCoinPurchaseSerializer(BaseCoinPurchaseSerializer):
    class Meta(BaseCoinPurchaseSerializer.Meta):
        fields = ('id', 'amount', 'price', 'status', 'created_at',)

# Advisor Serializers
class AdvisorUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = ('id', 'email', 'username', 'first_name', 'last_name', 'is_active',)

class AdvisorSerializer(serializers.ModelSerializer):
    user = AdvisorUserSerializer(read_only=True)
    rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    total_consultations = serializers.IntegerField(read_only=True)
    total_video_chats = serializers.IntegerField(read_only=True)
    total_phone_calls = serializers.IntegerField(read_only=True)

    class Meta:
        model = Advisor
        fields = '__all__'
        read_only_fields = ('id', 'rating', 'total_consultations', 'total_video_chats', 'total_phone_calls',)

class AdvisorNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta):
        fields = ('id', 'notification_type', 'title', 'message', 'is_read', 'created_at',)

class AdvisorWalletSerializer(BaseWalletSerializer):
    class Meta(BaseWalletSerializer.Meta):
        fields = ('id', 'balance', 'created_at', 'updated_at',)

class AdvisorTransactionSerializer(BaseTransactionSerializer):
    class Meta(BaseTransactionSerializer.Meta):
        fields = ('id', 'transaction_type', 'amount', 'description', 'created_at',)

class AdvisorCoinSerializer(BaseCoinSerializer):
    class Meta(BaseCoinSerializer.Meta):
        fields = ('id', 'amount', 'is_used', 'created_at',)

class AdvisorCoinTransactionSerializer(BaseCoinTransactionSerializer):
    class Meta(BaseCoinTransactionSerializer.Meta):
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at',)

class AdvisorCoinPurchaseSerializer(BaseCoinPurchaseSerializer):
    class Meta(BaseCoinPurchaseSerializer.Meta):
        fields = ('id', 'amount', 'price', 'status', 'created_at',)

# Admin Serializers
class AdminUserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        fields = '__all__'
        extra_kwargs = {'password': {'write_only': True}}

class AdminCustomerSerializer(BaseCustomerSerializer):
    class Meta(BaseCustomerSerializer.Meta):
        fields = '__all__'

class AdminNotificationSerializer(BaseNotificationSerializer):
    class Meta(BaseNotificationSerializer.Meta):
        fields = '__all__'

class AdminWalletSerializer(BaseWalletSerializer):
    class Meta(BaseWalletSerializer.Meta):
        fields = '__all__'

class AdminTransactionSerializer(BaseTransactionSerializer):
    class Meta(BaseTransactionSerializer.Meta):
        fields = '__all__'

class AdminCoinSerializer(BaseCoinSerializer):
    class Meta(BaseCoinSerializer.Meta):
        fields = '__all__'

class AdminCoinTransactionSerializer(BaseCoinTransactionSerializer):
    class Meta(BaseCoinTransactionSerializer.Meta):
        fields = '__all__'

class AdminCoinPurchaseSerializer(BaseCoinPurchaseSerializer):
    class Meta(BaseCoinPurchaseSerializer.Meta):
        fields = '__all__'

# Consultation and Service Serializers
class ConsultationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class ServiceAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceAvailability
        fields = '__all__'
        read_only_fields = ('id',)

class VideoChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoChat
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class PhoneCallSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhoneCall
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class FollowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follower
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ('id', 'created_at',)

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'completed_at', 'refunded_at')

    def validate(self, data):
        if data.get('amount', 0) <= 0:
            raise serializers.ValidationError({'amount': 'Amount must be greater than 0'})
        return data

class TransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )

    class Meta:
        model = Transaction
        fields = '__all__'

class WalletSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.00'),
        read_only=True
    )

    class Meta:
        model = Wallet
        fields = '__all__'

class CoinTransactionSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )

    class Meta:
        model = CoinTransaction
        fields = '__all__'

class CoinPurchaseSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )
    price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )

    class Meta:
        model = CoinPurchase
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal('0.01'),
        max_value=Decimal('999999.99')
    )

    class Meta:
        model = Order
        fields = '__all__'

class RatingSerializer(serializers.ModelSerializer):
    rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=1,
        min_value=Decimal('0.0'),
        max_value=Decimal('5.0')
    )

    class Meta:
        model = Rating
        fields = '__all__'

# Customer specific serializers
class CustomerTransactionSerializer(TransactionSerializer):
    pass

class CustomerWalletSerializer(WalletSerializer):
    pass

class CustomerCoinTransactionSerializer(CoinTransactionSerializer):
    pass

class CustomerCoinPurchaseSerializer(CoinPurchaseSerializer):
    pass

# Advisor specific serializers
class AdvisorTransactionSerializer(TransactionSerializer):
    pass

class AdvisorWalletSerializer(WalletSerializer):
    pass

class AdvisorCoinTransactionSerializer(CoinTransactionSerializer):
    pass

class AdvisorCoinPurchaseSerializer(CoinPurchaseSerializer):
    pass
