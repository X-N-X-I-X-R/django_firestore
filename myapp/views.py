from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, login
from django.core.mail import send_mail
from django.conf import settings
from .serializers import UserSerializer
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import CustomerRegistrationForm, AdvisorRegistrationForm
from django.utils.crypto import get_random_string
from django.core.signing import TimestampSigner
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for user management
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """
    Register a new user
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        
        # If registering as an advisor
        if request.data.get('registration_type') == 'advisor':
            user.is_active = False
            user.is_verified = False
            user.save()
            
            try:
                # Send verification email to the user
                token = generate_verification_token(user)
                current_site = get_current_site(request)
                verification_url = f"http://{current_site.domain}/api/verify-email/{token}/"
                
                subject = 'Verify your email address'
                message = f"""
Hi {user.username},

Thank you for registering as an advisor on our platform! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

Best regards,
The Team
"""
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                    fail_silently=False,
                )
                
                # Send email to admin
                admin_email = settings.ADMIN_EMAIL
                send_mail(
                    'New Advisor Registration',
                    f'A new advisor has registered:\n\n'
                    f'Name: {user.get_full_name()}\n'
                    f'Email: {user.email}\n'
                    f'Expertise: {user.expertise}\n'
                    f'Hourly Rate: ${user.hourly_rate}\n\n'
                    f'Please review their documents and verify their account.',
                    settings.DEFAULT_FROM_EMAIL,
                    [admin_email],
                    fail_silently=False,
                )
                
                return Response({
                    'message': 'Registration successful! Please check your email to verify your account.',
                    'user': serializer.data,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                # If email sending fails, delete the user
                user.delete()
                return Response({
                    'message': f'Registration failed: {str(e)}',
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # For regular users
        send_mail(
            'Welcome to Our Platform',
            f'Hi {user.username},\n\nWelcome to our platform! We are excited to have you on board.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )
        
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
def customer_register(request):
    """
    Register a new customer
    """
    if request.method == 'POST':
        if request.accepted_renderer.format == 'json':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # Send verification email
                try:
                    token = generate_verification_token(user)
                    current_site = get_current_site(request)
                    verification_url = f"http://{current_site.domain}/api/v1/verify-email/{token}/"
                    
                    subject = 'Verify your email address'
                    message = f"""
Hi {user.username},

Thank you for registering on our platform! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

Best regards,
The Team
"""
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    
                    return Response({
                        'message': 'Registration successful! Please check your email to verify your account.',
                        'user': serializer.data,
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    user.delete()
                    return Response({
                        'message': f'Registration failed: {str(e)}',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = CustomerRegistrationForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                messages.success(request, 'Registration successful! Welcome to our platform.')
                return redirect('home')
    else:
        form = CustomerRegistrationForm()
    return render(request, 'registration/customer_register.html', {'form': form})

def generate_verification_token(user):
    """Generate a verification token for the user"""
    signer = TimestampSigner()
    return signer.sign(user.email)

def send_verification_email(request, user):
    """Send verification email to the user"""
    try:
        token = generate_verification_token(user)
        current_site = get_current_site(request)
        verification_url = f"http://{current_site.domain}/api/v1/verify-email/{token}/"
        
        subject = 'Verify your email address'
        message = f"""
Hi {user.username},

Thank you for registering on our platform! Please verify your email address by clicking the link below:

{verification_url}

This link will expire in 24 hours.

Best regards,
The Team
"""
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    except Exception as e:
        raise Exception(f"Failed to send verification email: {str(e)}")

@api_view(['GET', 'POST'])
@permission_classes([AllowAny])
@csrf_exempt
def advisor_register(request):
    """
    Register a new advisor
    """
    if request.method == 'POST':
        if request.accepted_renderer.format == 'json':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                refresh = RefreshToken.for_user(user)
                
                # הגדרת המשתמש כמתין לאימות
                user.is_active = False
                user.is_verified = False
                user.save()
                
                try:
                    # שליחת מייל אימות למשתמש
                    send_verification_email(request, user)
                    
                    # שליחת מייל למנהל המערכת
                    admin_email = settings.ADMIN_EMAIL
                    send_mail(
                        'New Advisor Registration',
                        f'A new advisor has registered:\n\n'
                        f'Name: {user.get_full_name()}\n'
                        f'Email: {user.email}\n'
                        f'Expertise: {user.expertise}\n'
                        f'Hourly Rate: ${user.hourly_rate}\n\n'
                        f'Please review their documents and verify their account.',
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False,
                    )
                    
                    return Response({
                        'message': 'Registration successful! Please check your email to verify your account.',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # במקרה של שגיאה בשליחת המייל, נמחק את המשתמש
                    user.delete()
                    return Response({
                        'message': f'Registration failed: {str(e)}',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            form = AdvisorRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                # הגדרת המשתמש כמתין לאימות
                user.is_active = False
                user.is_verified = False
                user.save()
                
                # יצירת טוקן אבטחה
                refresh = RefreshToken.for_user(user)
                
                try:
                    # שליחת מייל אימות למשתמש
                    send_verification_email(request, user)
                    
                    # שליחת מייל למנהל המערכת
                    admin_email = settings.ADMIN_EMAIL
                    send_mail(
                        'New Advisor Registration',
                        f'A new advisor has registered:\n\n'
                        f'Name: {user.get_full_name()}\n'
                        f'Email: {user.email}\n'
                        f'Expertise: {user.expertise}\n'
                        f'Hourly Rate: ${user.hourly_rate}\n\n'
                        f'Please review their documents and verify their account.',
                        settings.DEFAULT_FROM_EMAIL,
                        [admin_email],
                        fail_silently=False,
                    )
                    
                    messages.success(request, 'Registration successful! Please check your email to verify your account.')
                    return Response({
                        'message': 'Registration successful! Please check your email to verify your account.',
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }, status=status.HTTP_201_CREATED)
                except Exception as e:
                    # במקרה של שגיאה בשליחת המייל, נמחק את המשתמש
                    user.delete()
                    messages.error(request, f'Registration failed: {str(e)}')
                    return Response({
                        'message': f'Registration failed: {str(e)}',
                    }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        form = AdvisorRegistrationForm()
    return render(request, 'registration/advisor_register.html', {'form': form})

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, token):
    """Verify user's email address"""
    try:
        signer = TimestampSigner()
        email = signer.unsign(token, max_age=86400)  # 24 hours
        user = User.objects.get(email=email)
        
        if user.is_verified:
            return Response({
                'message': 'Email already verified.'
            }, status=status.HTTP_200_OK)
        
        user.is_verified = True
        user.is_active = True
        user.save()
        
        return Response({
            'message': 'Email verified successfully! You can now log in.'
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({
            'message': f'Verification failed: {str(e)}'
        }, status=status.HTTP_400_BAD_REQUEST)

@login_required
def home(request):
    if request.user.is_advisor:
        return render(request, 'advisor_dashboard.html')
    return render(request, 'customer_dashboard.html') 