from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from ..serializers import UserSerializer
from ..models import User, Customer, Advisor

router = DefaultRouter()

@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generate verification token
        token = get_random_string(64)
        user.verification_token = token
        user.save()

        # Send verification email
        verification_url = f"{settings.SITE_URL}/verify-email/{token}/"
        send_mail(
            'Verify your email',
            f'Please click this link to verify your email: {verification_url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return Response({
            'message': 'Registration successful. Please check your email to verify your account.',
            'user': serializer.data
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token, is_verified=False)
        user.is_verified = True
        user.verification_token = ''
        user.save()
        return Response({'message': 'Email verified successfully'})
    except User.DoesNotExist:
        return Response({'error': 'Invalid verification token'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def home(request):
    user = request.user
    if hasattr(user, 'advisor_profile'):
        # User is an advisor
        return Response({
            'user_type': 'advisor',
            'profile': user.advisor_profile
        })
    elif hasattr(user, 'customer'):
        # User is a customer
        return Response({
            'user_type': 'customer',
            'profile': user.customer
        })
    else:
        return Response({
            'user_type': 'unknown',
            'profile': None
        }) 