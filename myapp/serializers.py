from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'registration_type',
                 'first_name', 'last_name', 'phone_number', 'country', 'birth_date',
                 'expertise', 'hourly_rate', 'verification_documents')
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
        return user 