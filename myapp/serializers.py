from rest_framework import serializers
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True)
    
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'password2', 'registration_type',
                 'first_name', 'last_name', 'phone_number', 'country', 'birth_date')
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        if data.get('password') != data.get('password2'):
            raise serializers.ValidationError("Passwords don't match")
        return data
    
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
            registration_type=validated_data.get('registration_type', 'customer')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user 