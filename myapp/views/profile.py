from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import CustomUser, Profile
from ..serializers import (
    ProfileSerializer,
    AdvisorProfileSerializer,
    CustomerProfileSerializer,
    UserSerializer
)
from ..permissions import IsOwnerOrReadOnly, IsAdvisorOrReadOnly, IsCustomerOrReadOnly
from ..log import setup_logger

logger = setup_logger(__name__)

class ProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing user profiles.
    Provides different views for advisors and customers.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    
    def get_queryset(self):
        """
        Return the profile for the current user
        """
        return Profile.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        """
        Return appropriate serializer class based on user type
        """
        if self.action in ['update', 'partial_update']:
            if self.request.user.is_advisor:
                return AdvisorProfileSerializer
            return CustomerProfileSerializer
        return super().get_serializer_class()
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """
        Get the current user's profile
        """
        serializer = self.get_serializer(request.user.profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_profile_picture(self, request):
        """
        Update the user's profile picture
        """
        profile = request.user.profile
        if 'profile_picture' not in request.FILES:
            return Response(
                {'error': 'No profile picture provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.profile_picture = request.FILES['profile_picture']
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_bio(self, request):
        """
        Update the user's bio
        """
        profile = request.user.profile
        bio = request.data.get('bio')
        
        if not bio:
            return Response(
                {'error': 'No bio provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        profile.bio = bio
        profile.save()
        
        serializer = self.get_serializer(profile)
        return Response(serializer.data)

class AdvisorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing advisor-specific profile information
    """
    serializer_class = AdvisorProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdvisorOrReadOnly]
    
    def get_queryset(self):
        """
        Return advisor profiles
        """
        return CustomUser.objects.filter(is_advisor=True)
    
    @action(detail=False, methods=['post'])
    def update_expertise(self, request):
        """
        Update advisor's expertise
        """
        expertise = request.data.get('expertise')
        if not expertise:
            return Response(
                {'error': 'No expertise provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.expertise = expertise
        request.user.save()
        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_hourly_rate(self, request):
        """
        Update advisor's hourly rate
        """
        hourly_rate = request.data.get('hourly_rate')
        if not hourly_rate:
            return Response(
                {'error': 'No hourly rate provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        request.user.hourly_rate = hourly_rate
        request.user.save()
        
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing customer-specific profile information
    """
    serializer_class = CustomerProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsCustomerOrReadOnly]
    
    def get_queryset(self):
        """
        Return customer profiles
        """
        return CustomUser.objects.filter(is_customer=True)
    
    @action(detail=False, methods=['post'])
    def update_personal_info(self, request):
        """
        Update customer's personal information
        """
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 