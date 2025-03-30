from rest_framework import serializers
from .models import CustomUser, Profile, Consultation, Review
from django.contrib.auth.password_validation import validate_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_picture', 'created_at', 'updated_at')
        read_only_fields = ('created_at', 'updated_at')

class AdvisorProfileSerializer(serializers.ModelSerializer):
    expertise = serializers.CharField(required=True)
    hourly_rate = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    is_verified = serializers.BooleanField(read_only=True)
    verification_documents = serializers.FileField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('expertise', 'hourly_rate', 'is_verified', 'verification_documents')

class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'phone_number', 'country', 'birth_date')

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'registration_type',
                 'first_name', 'last_name', 'phone_number', 'country', 'birth_date',
                 'expertise', 'hourly_rate', 'verification_documents', 'is_verified',
                 'profile')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            'birth_date': {'required': False},
            'expertise': {'required': False},
            'hourly_rate': {'required': False},
            'verification_documents': {'required': False}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone_number=validated_data.get('phone_number'),
            country=validated_data.get('country'),
            birth_date=validated_data.get('birth_date'),
            registration_type=validated_data.get('registration_type', 'customer'),
            expertise=validated_data.get('expertise'),
            hourly_rate=validated_data.get('hourly_rate'),
            verification_documents=validated_data.get('verification_documents')
        )
        user.set_password(validated_data['password'])
        user.save()
        
        # Create profile
        Profile.objects.create(user=user)
        
        return user

class ConsultationSerializer(serializers.ModelSerializer):
    advisor_name = serializers.CharField(source='advisor.get_full_name', read_only=True)
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = Consultation
        fields = ('id', 'title', 'description', 'price', 'duration', 'status',
                 'created_at', 'updated_at', 'advisor', 'customer',
                 'advisor_name', 'customer_name')
        read_only_fields = ('created_at', 'updated_at', 'advisor', 'customer')

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='customer.get_full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ('id', 'consultation', 'customer', 'rating', 'comment',
                 'created_at', 'customer_name')
        read_only_fields = ('created_at', 'customer') 