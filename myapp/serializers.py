from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=False)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'phone_number', 
                 'country', 'bio', 'birth_date', 'profile_picture', 'date_joined', 
                 'is_active', 'registration_type', 'expertise', 'hourly_rate', 
                 'verification_documents', 'is_verified')
        read_only_fields = ('date_joined', 'is_active', 'is_verified')
        extra_kwargs = {
            'password': {'write_only': True},
            'expertise': {'required': False},
            'hourly_rate': {'required': False},
            'verification_documents': {'required': False},
            'registration_type': {'required': True},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if 'country' in data and data['country']:
            data['country'] = str(data['country'])
        return data

    def validate(self, data):
        if 'password' in data:
            if 'password2' not in data:
                raise serializers.ValidationError("Please confirm your password.")
            if data['password'] != data['password2']:
                raise serializers.ValidationError("Passwords do not match.")
            data.pop('password2')
        
        # Validate advisor-specific fields
        if data.get('registration_type') == 'advisor':
            if not data.get('expertise'):
                raise serializers.ValidationError({"expertise": "Expertise is required for advisors."})
            if not data.get('hourly_rate'):
                raise serializers.ValidationError({"hourly_rate": "Hourly rate is required for advisors."})
            if data.get('hourly_rate', 0) <= 0:
                raise serializers.ValidationError({"hourly_rate": "Hourly rate must be greater than 0."})
        
        return data

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        registration_type = validated_data.get('registration_type')
        
        # Set default values for advisor
        if registration_type == 'advisor':
            validated_data['is_active'] = False
            validated_data['is_verified'] = False
        
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user 