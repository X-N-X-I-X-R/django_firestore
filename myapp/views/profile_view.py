from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.routers import DefaultRouter
from django.shortcuts import get_object_or_404
from ..models import User, Customer, Advisor
from ..serializers import UserSerializer, CustomerSerializer, AdvisorSerializer
from ..permissions import IsOwnerOrAdmin

router = DefaultRouter()

class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrAdmin]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    @action(detail=False, methods=['get'])
    def me(self, request):
        user = request.user
        if hasattr(user, 'advisor_profile'):
            serializer = AdvisorSerializer(user.advisor_profile)
            return Response({
                'user_type': 'advisor',
                'profile': serializer.data
            })
        elif hasattr(user, 'customer'):
            serializer = CustomerSerializer(user.customer)
            return Response({
                'user_type': 'customer',
                'profile': serializer.data
            })
        else:
            serializer = UserSerializer(user)
            return Response({
                'user_type': 'unknown',
                'profile': serializer.data
            })

    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        user = request.user
        if hasattr(user, 'advisor_profile'):
            serializer = AdvisorSerializer(user.advisor_profile, data=request.data, partial=True)
        elif hasattr(user, 'customer'):
            serializer = CustomerSerializer(user.customer, data=request.data, partial=True)
        else:
            serializer = UserSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

router.register(r'profile', ProfileViewSet, basename='profile') 