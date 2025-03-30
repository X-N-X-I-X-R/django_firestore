from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import auth

router = DefaultRouter()
router.register(r'users', auth.UserViewSet)

urlpatterns = [
    # API endpoints
    path('v1/', include(router.urls)),
    
    # Authentication endpoints
    path('v1/auth/register/', auth.register_user, name='register'),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/verify-email/<str:token>/', auth.verify_email, name='verify_email'),
    
    # Home page (varies by user type)
    path('v1/home/', auth.home, name='home'),
] 