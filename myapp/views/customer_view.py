from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from rest_framework.pagination import PageNumberPagination
from ..models import (
    Customer, Notification, Wallet, Transaction,
    Consultation, VideoChat, PhoneCall, Order,
    Rating, Review, Follower, Subscription,
    Coin, CoinTransaction, CoinPurchase
)
from ..serializers import (
    CustomerUserSerializer, CustomerNotificationSerializer,
    CustomerWalletSerializer, CustomerTransactionSerializer,
    CustomerCoinSerializer, CustomerCoinTransactionSerializer,
    CustomerCoinPurchaseSerializer, ConsultationSerializer,
    VideoChatSerializer, PhoneCallSerializer, OrderSerializer,
    RatingSerializer, ReviewSerializer, FollowerSerializer,
    SubscriptionSerializer
)
from ..permissions import IsCustomer, IsOwnerOrAdmin
from ..exceptions import InsufficientFundsError, InvalidStatusError

class BaseCustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsCustomer]
    pagination_class = PageNumberPagination
    cache_timeout = 300  # 5 minutes

    def get_queryset(self):
        cache_key = f'customer_{self.request.user.id}_{self.basename}_queryset'
        queryset = cache.get(cache_key)
        
        if queryset is None:
            queryset = super().get_queryset()
            cache.set(cache_key, queryset, self.cache_timeout)
        
        return queryset

    def handle_exception(self, exc):
        if isinstance(exc, InsufficientFundsError):
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        if isinstance(exc, InvalidStatusError):
            return Response(
                {'error': str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().handle_exception(exc)

class CustomerViewSet(BaseCustomerViewSet):
    serializer_class = CustomerUserSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Customer.objects.none()
        return Customer.objects.filter(user=self.request.user)

class NotificationViewSet(BaseCustomerViewSet):
    serializer_class = CustomerNotificationSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        cache.delete(f'customer_{request.user.id}_notification_queryset')
        return Response({'status': 'notification marked as read'})

class WalletViewSet(BaseCustomerViewSet):
    serializer_class = CustomerWalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response(
                {'error': 'Valid amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            wallet.balance += amount
            wallet.save()
            cache.delete(f'customer_{request.user.id}_wallet_queryset')
            return Response({'status': 'deposit successful'})

class TransactionViewSet(BaseCustomerViewSet):
    serializer_class = CustomerTransactionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        # Get the user's wallet first
        wallet = Wallet.objects.get(user=self.request.user)
        return Transaction.objects.filter(wallet=wallet).select_related('wallet')

class CustomerCoinViewSet(BaseCustomerViewSet):
    serializer_class = CustomerCoinSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Coin.objects.none()
        return Coin.objects.filter(wallet__user=self.request.user).select_related('wallet')

class CustomerCoinTransactionViewSet(BaseCustomerViewSet):
    serializer_class = CustomerCoinTransactionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CoinTransaction.objects.none()
        return CoinTransaction.objects.filter(wallet__user=self.request.user).select_related('wallet')

class CustomerCoinPurchaseViewSet(BaseCustomerViewSet):
    serializer_class = CustomerCoinPurchaseSerializer

    def get_queryset(self):
        return CoinPurchase.objects.filter(user=self.request.user).select_related('user')

    @action(detail=True, methods=['post'])
    def initiate_purchase(self, request, pk=None):
        purchase = self.get_object()
        if purchase.status != 'pending':
            raise InvalidStatusError('Purchase is not in pending status')

        with transaction.atomic():
            # Simulate payment processing
            purchase.status = 'completed'
            purchase.completed_at = timezone.now()
            purchase.save()

            # Create coin transaction
            CoinTransaction.objects.create(
                user=request.user,
                amount=purchase.amount,
                transaction_type='purchase',
                description=f'Purchase of {purchase.amount} coins'
            )
            cache.delete(f'customer_{request.user.id}_coin_purchase_queryset')
            cache.delete(f'customer_{request.user.id}_coin_transaction_queryset')

        return Response({'status': 'purchase completed'})

class CustomerConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Consultation.objects.none()
        return Consultation.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerVideoChatViewSet(viewsets.ModelViewSet):
    serializer_class = VideoChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return VideoChat.objects.none()
        return VideoChat.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerPhoneCallViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneCallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PhoneCall.objects.none()
        return PhoneCall.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerOrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerRatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rating.objects.none()
        return Rating.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerFollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Follower.objects.none()
        return Follower.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

class CustomerSubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        return Subscription.objects.filter(customer=self.request.user.customer)

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer) 