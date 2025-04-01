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
    Advisor, Notification, Wallet, Transaction,
    Consultation, VideoChat, PhoneCall, Order,
    Rating, Review, Follower, Subscription,
    Coin, CoinTransaction, CoinPurchase, ServiceAvailability
)
from ..serializers import (
    AdvisorSerializer, AdvisorNotificationSerializer,
    AdvisorWalletSerializer, AdvisorTransactionSerializer,
    AdvisorCoinSerializer, AdvisorCoinTransactionSerializer,
    AdvisorCoinPurchaseSerializer, ConsultationSerializer,
    VideoChatSerializer, PhoneCallSerializer, OrderSerializer,
    RatingSerializer, ReviewSerializer, FollowerSerializer,
    SubscriptionSerializer, ServiceAvailabilitySerializer
)
from ..permissions import IsAdvisor, IsOwnerOrAdmin
from ..exceptions import InsufficientFundsError, InvalidStatusError

class BaseAdvisorViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdvisor]
    pagination_class = PageNumberPagination
    cache_timeout = 300  # 5 minutes

    def get_queryset(self):
        cache_key = f'advisor_{self.request.user.id}_{self.basename}_queryset'
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

class AdvisorViewSet(viewsets.ModelViewSet):
    serializer_class = AdvisorSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Advisor.objects.none()
        return Advisor.objects.filter(user=self.request.user)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        advisor = self.get_object()
        cache_key = f'advisor_{advisor.id}_statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_consultations': Consultation.objects.filter(advisor=advisor).count(),
                'total_earnings': Order.objects.filter(advisor=advisor, status='completed').aggregate(Sum('amount'))['amount__sum'] or 0,
                'average_rating': Rating.objects.filter(advisor=advisor).aggregate(Avg('rating'))['rating__avg'] or 0,
                'total_followers': Follower.objects.filter(advisor=advisor).count(),
            }
            cache.set(cache_key, stats, self.cache_timeout)
        
        return Response(stats)

class NotificationViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorNotificationSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Notification.objects.none()
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        cache.delete(f'advisor_{request.user.id}_notification_queryset')
        return Response({'status': 'notification marked as read'})

class WalletViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorWalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(user=self.request.user)

class TransactionViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorTransactionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Transaction.objects.none()
        # Get the user's wallet first
        wallet = Wallet.objects.get(user=self.request.user)
        return Transaction.objects.filter(wallet=wallet).select_related('wallet')

class AdvisorCoinViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorCoinSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Coin.objects.none()
        return Coin.objects.filter(wallet__user=self.request.user).select_related('wallet')

class AdvisorCoinTransactionViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorCoinTransactionSerializer

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return CoinTransaction.objects.none()
        return CoinTransaction.objects.filter(wallet__user=self.request.user).select_related('wallet')

    @action(detail=False, methods=['post'])
    def withdraw(self, request):
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response(
                {'error': 'Valid amount is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            # Check balance
            wallet = Wallet.objects.get(user=request.user)
            if wallet.balance < amount:
                raise InsufficientFundsError('Insufficient funds for withdrawal')

            # Create withdrawal transaction
            CoinTransaction.objects.create(
                wallet=wallet,
                amount=amount,
                transaction_type='withdrawal',
                description=f'Withdrawal of {amount} coins'
            )
            cache.delete(f'advisor_{request.user.id}_coin_transaction_queryset')
            cache.delete(f'advisor_{request.user.id}_wallet_queryset')

        return Response({'status': 'withdrawal initiated'})

class AdvisorCoinPurchaseViewSet(BaseAdvisorViewSet):
    serializer_class = AdvisorCoinPurchaseSerializer

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
            cache.delete(f'advisor_{request.user.id}_coin_purchase_queryset')
            cache.delete(f'advisor_{request.user.id}_coin_transaction_queryset')

        return Response({'status': 'purchase completed'})

class ConsultationViewSet(viewsets.ModelViewSet):
    serializer_class = ConsultationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Consultation.objects.none()
        return Consultation.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class ServiceAvailabilityViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return ServiceAvailability.objects.none()
        return ServiceAvailability.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class VideoChatViewSet(viewsets.ModelViewSet):
    serializer_class = VideoChatSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return VideoChat.objects.none()
        return VideoChat.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class PhoneCallViewSet(viewsets.ModelViewSet):
    serializer_class = PhoneCallSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PhoneCall.objects.none()
        return PhoneCall.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class RatingViewSet(viewsets.ModelViewSet):
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Rating.objects.none()
        return Rating.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class FollowerViewSet(viewsets.ModelViewSet):
    serializer_class = FollowerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Follower.objects.none()
        return Follower.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor)

class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Subscription.objects.none()
        return Subscription.objects.filter(advisor=self.request.user.advisor)

    def perform_create(self, serializer):
        serializer.save(advisor=self.request.user.advisor) 