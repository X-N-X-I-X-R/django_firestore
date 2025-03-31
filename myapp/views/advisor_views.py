from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from django_filters import rest_framework as filters
from ..models import AdvisorApplication
from ..serializers import AdvisorApplicationSerializer
from ..permissions import IsAdmin

class AdvisorApplicationFilter(filters.FilterSet):
    status = filters.ChoiceFilter(choices=AdvisorApplication.STATUS_CHOICES)
    submitted_at = filters.DateFromToRangeFilter()
    specialization = filters.CharFilter(lookup_expr='icontains')
    years_of_experience = filters.NumberFilter()
    years_of_experience_gte = filters.NumberFilter(field_name='years_of_experience', lookup_expr='gte')
    
    class Meta:
        model = AdvisorApplication
        fields = ['status', 'submitted_at', 'specialization', 'years_of_experience']

class AdvisorApplicationViewSet(viewsets.ModelViewSet):
    queryset = AdvisorApplication.objects.all()
    serializer_class = AdvisorApplicationSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = AdvisorApplicationFilter
    
    def get_permissions(self):
        if self.action in ['create', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        elif self.action in ['list', 'approve', 'reject']:
            permission_classes = [IsAdmin]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        advisor_application = serializer.save()
        
        # Send notification email to admin
        admin_email = settings.ADMIN_EMAIL
        if admin_email:
            send_mail(
                'New Advisor Application',
                f'A new advisor application has been submitted by {advisor_application.user.email}',
                settings.DEFAULT_FROM_EMAIL,
                [admin_email],
                fail_silently=True,
            )
        
        return Response({
            'message': 'Your application has been submitted successfully. We will review it and get back to you soon.',
            'application': AdvisorApplicationSerializer(advisor_application).data
        }, status=status.HTTP_201_CREATED)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Allow only admin or the applicant to view the application
        if not request.user.is_staff and request.user != instance.user:
            return Response(
                {'error': 'You do not have permission to view this application.'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        application = self.get_object()
        if application.status != 'pending':
            return Response({
                'error': 'This application has already been processed.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        application.approve()
        
        # Send approval email
        send_mail(
            'Your advisor application has been approved!',
            f'''Congratulations! Your application to become an advisor has been approved.
            You can now log in and start providing consultations.
            
            Best regards,
            The Team''',
            settings.DEFAULT_FROM_EMAIL,
            [application.user.email],
            fail_silently=True,
        )
        
        return Response({
            'message': 'Advisor application approved successfully.',
            'application': AdvisorApplicationSerializer(application).data
        })

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        application = self.get_object()
        if application.status != 'pending':
            return Response({
                'error': 'This application has already been processed.'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        notes = request.data.get('notes', '')
        application.reject(notes=notes)
        
        # Send rejection email
        send_mail(
            'Update on your advisor application',
            f'''We have reviewed your application to become an advisor.
            Unfortunately, we cannot approve your application at this time.
            
            {notes if notes else 'Thank you for your interest.'}
            
            Best regards,
            The Team''',
            settings.DEFAULT_FROM_EMAIL,
            [application.user.email],
            fail_silently=True,
        )
        
        return Response({
            'message': 'Advisor application rejected.',
            'application': AdvisorApplicationSerializer(application).data
        }) 