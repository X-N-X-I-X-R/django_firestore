from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.views.generic import RedirectView
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    # API endpoints
    path('v1/', include(router.urls)),
    
    # Authentication endpoints
    path('v1/auth/register/', views.register_user, name='register'),
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/verify-email/<str:token>/', views.verify_email, name='verify_email'),
    
    # נתיבי הרשמה
    path('v1/register/customer/', views.customer_register, name='customer_register'),
    path('v1/register/advisor/', views.advisor_register, name='advisor_register'),
    
    # דף הבית (משתנה לפי סוג המשתמש)
    path('v1/home/', views.home, name='home'),
] 