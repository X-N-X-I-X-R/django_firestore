from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from django.utils import timezone
from django.core.cache import cache
from django.conf import settings
from django.db.models import Sum, Avg, Count
from rest_framework.pagination import PageNumberPagination
from ..models import (
    Coin, CoinTransaction, CoinPurchase,
    Order, Payment
)
from ..serializers import (
    AdminCoinSerializer, AdminCoinTransactionSerializer,
    AdminCoinPurchaseSerializer, PaymentSerializer
)
from ..permissions import IsAdmin, IsOwnerOrAdmin
from ..exceptions import InsufficientFundsError, InvalidStatusError

class BasePaymentViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsAdmin]
    pagination_class = PageNumberPagination
    cache_timeout = 300  # 5 minutes

    def get_queryset(self):
        cache_key = f'payment_{self.request.user.id}_{self.basename}_queryset'
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

class CoinViewSet(BasePaymentViewSet):
    serializer_class = AdminCoinSerializer

    def get_queryset(self):
        return Coin.objects.all().select_related('user')

    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        coin = self.get_object()
        if coin.is_used:
            raise InvalidStatusError('Coin has already been used')
        return Response({'status': 'coin is valid'})

class CoinTransactionViewSet(BasePaymentViewSet):
    serializer_class = AdminCoinTransactionSerializer

    def get_queryset(self):
        return CoinTransaction.objects.all().select_related('user')

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        cache_key = 'coin_transaction_statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_transactions': CoinTransaction.objects.count(),
                'total_amount': CoinTransaction.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
                'transactions_by_type': CoinTransaction.objects.values('transaction_type').annotate(
                    count=Count('id'),
                    total=Sum('amount')
                ),
                'recent_transactions': CoinTransaction.objects.order_by('-created_at')[:10]
            }
            cache.set(cache_key, stats, self.cache_timeout)
        
        return Response(stats)

class CoinPurchaseViewSet(BasePaymentViewSet):
    serializer_class = AdminCoinPurchaseSerializer

    def get_queryset(self):
        return CoinPurchase.objects.all().select_related('user')

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
                user=purchase.user,
                amount=purchase.amount,
                transaction_type='purchase',
                description=f'Purchase of {purchase.amount} coins'
            )
            cache.delete(f'payment_{request.user.id}_coin_purchase_queryset')
            cache.delete(f'payment_{request.user.id}_coin_transaction_queryset')

        return Response({'status': 'purchase completed'})

class PaymentViewSet(BasePaymentViewSet):
    serializer_class = PaymentSerializer

    def get_queryset(self):
        return Payment.objects.all().select_related('user', 'order')

    @action(detail=True, methods=['post'])
    def process_payment(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'pending':
            raise InvalidStatusError('Payment is not in pending status')

        with transaction.atomic():
            # Simulate payment processing
            payment.status = 'completed'
            payment.completed_at = timezone.now()
            payment.save()

            # Update order status
            order = payment.order
            order.status = 'paid'
            order.save()

            # Create coin transaction for advisor
            advisor = order.advisor
            advisor_amount = order.amount * (1 - order.platform_commission)
            CoinTransaction.objects.create(
                user=advisor.user,
                amount=advisor_amount,
                transaction_type='payment',
                description=f'Payment for order {order.id}'
            )
            cache.delete(f'payment_{request.user.id}_payment_queryset')
            cache.delete(f'payment_{request.user.id}_coin_transaction_queryset')

        return Response({'status': 'payment completed'})

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        payment = self.get_object()
        if payment.status != 'completed':
            raise InvalidStatusError('Payment is not completed')

        with transaction.atomic():
            # Simulate refund processing
            payment.status = 'refunded'
            payment.refunded_at = timezone.now()
            payment.save()

            # Update order status
            order = payment.order
            order.status = 'refunded'
            order.save()

            # Create refund transaction
            CoinTransaction.objects.create(
                user=payment.user,
                amount=payment.amount,
                transaction_type='refund',
                description=f'Refund for payment {payment.id}'
            )
            cache.delete(f'payment_{request.user.id}_payment_queryset')
            cache.delete(f'payment_{request.user.id}_coin_transaction_queryset')

        return Response({'status': 'refund completed'})

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        cache_key = 'payment_statistics'
        stats = cache.get(cache_key)
        
        if stats is None:
            stats = {
                'total_payments': Payment.objects.count(),
                'total_amount': Payment.objects.aggregate(Sum('amount'))['amount__sum'] or 0,
                'payments_by_status': Payment.objects.values('status').annotate(
                    count=Count('id'),
                    total=Sum('amount')
                ),
                'recent_payments': Payment.objects.order_by('-created_at')[:10]
            }
            cache.set(cache_key, stats, self.cache_timeout)
        
        return Response(stats)

    @action(detail=False, methods=['post'])
    def process_withdrawal(self, request):
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response({
                'message': 'Valid amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # TODO: Check user's coin balance
                # For now, simulate successful withdrawal
                CoinTransaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='withdrawal',
                    description=f'Withdrawal of {amount} coins'
                )

                return Response({
                    'message': 'Withdrawal processed successfully',
                    'amount': amount
                })
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def process_deposit(self, request):
        amount = request.data.get('amount')
        if not amount or amount <= 0:
            return Response({
                'message': 'Valid amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # TODO: Integrate with actual payment processor
                # For now, simulate successful deposit
                CoinTransaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='deposit',
                    description=f'Deposit of {amount} coins'
                )

                return Response({
                    'message': 'Deposit processed successfully',
                    'amount': amount
                })
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def process_coins_transfer(self, request):
        amount = request.data.get('amount')
        recipient_id = request.data.get('recipient_id')
        if not amount or amount <= 0 or not recipient_id:
            return Response({
                'message': 'Valid amount and recipient ID are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                # TODO: Check sender's coin balance
                # For now, simulate successful transfer
                CoinTransaction.objects.create(
                    user=request.user,
                    amount=amount,
                    transaction_type='transfer',
                    description=f'Transfer of {amount} coins to user {recipient_id}'
                )

                return Response({
                    'message': 'Transfer processed successfully',
                    'amount': amount,
                    'recipient_id': recipient_id
                })
        except Exception as e:
            return Response({
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST) 