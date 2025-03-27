from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Profile, Consultation, Message, Review

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    Provides a comprehensive interface for managing user accounts,
    including advisor verification and user permissions.
    """
    list_display = ('username', 'email', 'phone_number', 'country', 'is_active', 'is_staff', 'is_advisor', 'is_customer', 'is_verified')
    list_filter = ('is_active', 'is_staff', 'country', 'is_advisor', 'is_customer', 'is_verified')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    list_per_page = 25
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'country', 'bio', 'birth_date', 'profile_picture')}),
        ('Registration Type', {'fields': ('registration_type', 'is_advisor', 'is_customer')}),
        ('Advisor Info', {'fields': ('expertise', 'hourly_rate', 'is_verified', 'verification_documents'), 'classes': ('collapse',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'registration_type'),
        }),
    )

    def verify_advisors(self, request, queryset):
        """Action to verify selected advisors."""
        queryset.update(is_verified=True)
    verify_advisors.short_description = "Verify selected advisors"

    actions = ['verify_advisors']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin interface for Profile model.
    Manages user profiles with their associated information and timestamps.
    """
    list_display = ('user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')
    search_fields = ('user__username', 'user__email', 'bio')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    raw_id_fields = ['user']

@admin.register(Consultation)
class ConsultationAdmin(admin.ModelAdmin):
    """
    Admin interface for Consultation model.
    Manages consultation sessions between advisors and customers,
    including pricing, duration, and status tracking.
    """
    list_display = ('title', 'advisor', 'customer', 'price', 'duration', 'status', 'created_at')
    list_filter = ('status', 'created_at', 'advisor', 'customer')
    search_fields = ('title', 'description', 'advisor__username', 'customer__username')
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 25
    date_hierarchy = 'created_at'
    raw_id_fields = ['advisor', 'customer']
    
    fieldsets = (
        (None, {'fields': ('title', 'description', 'price', 'duration', 'status')}),
        ('Participants', {'fields': ('advisor', 'customer')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

    def mark_as_completed(self, request, queryset):
        """Action to mark selected consultations as completed."""
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected consultations as completed"

    actions = ['mark_as_completed']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """
    Admin interface for Message model.
    Manages communication between users within consultations,
    including read status and timestamps.
    """
    list_display = ('sender', 'receiver', 'consultation', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at', 'sender', 'receiver', 'consultation')
    search_fields = ('content', 'sender__username', 'receiver__username')
    readonly_fields = ('created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    raw_id_fields = ['sender', 'receiver', 'consultation']
    
    fieldsets = (
        (None, {'fields': ('content', 'is_read')}),
        ('Participants', {'fields': ('sender', 'receiver', 'consultation')}),
        ('Timestamp', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

    def mark_as_read(self, request, queryset):
        """Action to mark selected messages as read."""
        queryset.update(is_read=True)
    mark_as_read.short_description = "Mark selected messages as read"

    actions = ['mark_as_read']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin interface for Review model.
    Manages customer reviews for consultations,
    including ratings and comments.
    """
    list_display = ('consultation', 'customer', 'rating', 'created_at')
    list_filter = ('rating', 'created_at', 'customer')
    search_fields = ('comment', 'customer__username', 'consultation__title')
    readonly_fields = ('created_at',)
    list_per_page = 25
    date_hierarchy = 'created_at'
    raw_id_fields = ['consultation', 'customer']
    
    fieldsets = (
        (None, {'fields': ('rating', 'comment')}),
        ('Relations', {'fields': ('consultation', 'customer')}),
        ('Timestamp', {'fields': ('created_at',), 'classes': ('collapse',)}),
    )

