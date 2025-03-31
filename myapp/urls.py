from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    auth_view, profile_view, advisor_view,
    customer_view, payments_view
)
from .views.advisor_views import AdvisorApplicationViewSet

router = DefaultRouter()

# Advisor URLs
router.register(r'advisors', advisor_view.AdvisorViewSet, basename='advisor')
router.register(r'consultations', advisor_view.ConsultationViewSet, basename='consultation')
router.register(r'service-availability', advisor_view.ServiceAvailabilityViewSet, basename='service-availability')
router.register(r'video-chats', advisor_view.VideoChatViewSet, basename='video-chat')
router.register(r'phone-calls', advisor_view.PhoneCallViewSet, basename='phone-call')
router.register(r'orders', advisor_view.OrderViewSet, basename='order')
router.register(r'advisor-ratings', advisor_view.RatingViewSet, basename='advisor-rating')
router.register(r'advisor-reviews', advisor_view.ReviewViewSet, basename='advisor-review')
router.register(r'advisor-followers', advisor_view.FollowerViewSet, basename='advisor-follower')
router.register(r'advisor-subscriptions', advisor_view.SubscriptionViewSet, basename='advisor-subscription')
router.register(r'advisor-coins', advisor_view.AdvisorCoinViewSet, basename='advisor-coin')
router.register(r'advisor-coin-transactions', advisor_view.AdvisorCoinTransactionViewSet, basename='advisor-coin-transaction')
router.register(r'advisor-coin-purchases', advisor_view.AdvisorCoinPurchaseViewSet, basename='advisor-coin-purchase')
router.register(r'advisor-applications', AdvisorApplicationViewSet)

# Customer URLs
router.register(r'customers', customer_view.CustomerViewSet, basename='customer')
router.register(r'notifications', customer_view.NotificationViewSet, basename='notification')
router.register(r'wallets', customer_view.WalletViewSet, basename='wallet')
router.register(r'transactions', customer_view.TransactionViewSet, basename='transaction')
router.register(r'customer-consultations', customer_view.CustomerConsultationViewSet, basename='customer-consultation')
router.register(r'customer-video-chats', customer_view.CustomerVideoChatViewSet, basename='customer-video-chat')
router.register(r'customer-phone-calls', customer_view.CustomerPhoneCallViewSet, basename='customer-phone-call')
router.register(r'customer-orders', customer_view.CustomerOrderViewSet, basename='customer-order')
router.register(r'customer-ratings', customer_view.CustomerRatingViewSet, basename='customer-rating')
router.register(r'customer-reviews', customer_view.CustomerReviewViewSet, basename='customer-review')
router.register(r'customer-followers', customer_view.CustomerFollowerViewSet, basename='customer-follower')
router.register(r'customer-subscriptions', customer_view.CustomerSubscriptionViewSet, basename='customer-subscription')
router.register(r'customer-coins', customer_view.CustomerCoinViewSet, basename='customer-coin')
router.register(r'customer-coin-transactions', customer_view.CustomerCoinTransactionViewSet, basename='customer-coin-transaction')
router.register(r'customer-coin-purchases', customer_view.CustomerCoinPurchaseViewSet, basename='customer-coin-purchase')

# Payment URLs
router.register(r'coins', payments_view.CoinViewSet, basename='coin')
router.register(r'coin-transactions', payments_view.CoinTransactionViewSet, basename='coin-transaction')
router.register(r'coin-purchases', payments_view.CoinPurchaseViewSet, basename='coin-purchase')
router.register(r'payments', payments_view.PaymentViewSet, basename='payment')

urlpatterns = [
    # API v1 endpoints
    path('api/v1/', include(router.urls)),
    path('api/v1/auth/', include(auth_view.router.urls)),
    path('api/v1/profile/', include(profile_view.router.urls)),
    
    # Authentication endpoints
    path('api/v1/auth/register/', auth_view.register_user, name='register'),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/auth/verify-email/<str:token>/', auth_view.verify_email, name='verify_email'),
    
    # Home page (varies by user type)
    path('api/v1/home/', auth_view.home, name='home'),
] 