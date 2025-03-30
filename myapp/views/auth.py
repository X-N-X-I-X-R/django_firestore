from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.core.cache import cache
from django.conf import settings
from ..serializers import UserSerializer
from ..services.auth_service import AuthService
from ..forms.auth_forms import CustomerRegistrationForm, AdvisorRegistrationForm
from ..utils.phone_utils import PhoneNumberFormatter
from ..log import setup_logger
import hashlib
import time

logger = setup_logger(__name__)
User = get_user_model()

class SmartThrottle:
    """
    Professional throttling system that combines IP and user tracking
    with rate limiting and security measures
    """
    def __init__(self, rate_limit=5, time_window=3600):
        self.rate_limit = rate_limit
        self.time_window = time_window

    def get_client_identifier(self, request):
        """
        Generate a unique identifier for the client
        Combines IP address with additional security measures
        """
        # Get IP address
        ip = request.META.get('REMOTE_ADDR')
        
        # Get user agent
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        # Create a unique identifier using IP and user agent
        identifier = f"{ip}:{user_agent}"
        
        # Hash the identifier for security
        return hashlib.sha256(identifier.encode()).hexdigest()

    def is_rate_limited(self, request):
        """
        Check if the request should be rate limited
        """
        identifier = self.get_client_identifier(request)
        cache_key = f"throttle_{identifier}"
        
        # Get current attempts
        attempts = cache.get(cache_key, 0)
        
        # Check if rate limit exceeded
        if attempts >= self.rate_limit:
            logger.warning(f"Rate limit exceeded for identifier: {identifier}")
            return True
            
        # Increment attempts
        cache.set(cache_key, attempts + 1, self.time_window)
        return False

class RegistrationRateThrottle(SmartThrottle):
    """
    Throttle for registration attempts
    """
    def __init__(self):
        super().__init__(rate_limit=5, time_window=3600)  # 5 attempts per hour

class VerificationRateThrottle(SmartThrottle):
    """
    Throttle for email verification attempts
    """
    def __init__(self):
        super().__init__(rate_limit=10, time_window=3600)  # 10 attempts per hour

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Filter users based on user type
        """
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    def get_permissions(self):
        """
        Set permissions based on action
        """
        if self.action in ['create']:
            return [AllowAny()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        """
        Create a new user
        """
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        """
        Create user and send verification email
        """
        user = serializer.save()
        if not user.is_verified:
            token = AuthService.generate_verification_token(user)
            verification_url = AuthService.get_verification_url(self.request, token)
            AuthService.send_verification_email(user, verification_url, user.is_advisor)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user with smart throttling
    """
    # Check rate limiting
    throttle = RegistrationRateThrottle()
    if throttle.is_rate_limited(request):
        return Response({
            'error': 'Too many registration attempts. Please try again later.'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    logger.info(f"New registration attempt - User data: {request.data}")
    
    # Convert password1 to password if needed
    data = request.data.copy()
    if 'password1' in data:
        data['password'] = data.pop('password1')
    
    # Handle advisor registration without verification documents
    if data.get('registration_type') == 'advisor' and 'verification_documents' not in request.FILES:
        data['verification_documents'] = None
    
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        try:
            # Save user
            user = serializer.save()
            user.is_active = False
            user.is_verified = False
            user.save()
            
            # Generate verification URL and tokens
            token = AuthService.generate_verification_token(user)
            verification_url = AuthService.get_verification_url(request, token)
            tokens = AuthService.generate_tokens(user)
            
            # Send verification email
            AuthService.send_verification_email(user, verification_url, user.is_advisor)
            
            return Response({
                'message': 'Registration successful. Please check your email to verify your account.',
                'tokens': tokens
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            user.delete()  # Clean up if something goes wrong
            return Response({
                'message': f'Registration failed: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    """
    Verify user's email address with smart throttling
    """
    # Check rate limiting
    throttle = VerificationRateThrottle()
    if throttle.is_rate_limited(request):
        return Response({
            'error': 'Too many verification attempts. Please try again later.'
        }, status=status.HTTP_429_TOO_MANY_REQUESTS)
    
    try:
        # Verify token and get email
        email = AuthService.verify_token(token)
        
        # Get user and verify
        user = User.objects.get(email=email)
        user.is_verified = True
        user.is_active = True
        user.save()
        
        # Send admin notification after successful verification
        AuthService.send_admin_notification(user, user.is_advisor)
        
        return Response({
            'message': 'Email verified successfully. You can now log in.'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Email verification failed: {str(e)}")
        return Response({
            'message': f'Email verification failed: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@login_required
def home(request):
    if request.user.is_advisor:
        return render(request, 'advisor_dashboard.html')
    return render(request, 'customer_dashboard.html') 