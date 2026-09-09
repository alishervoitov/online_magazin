from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'avatar', 'phone_number', 'birth_date', 'gender',
            'region', 'district', 'address', 'postal_code',
            'loyalty_points', 'is_verified'
        ]
        read_only_fields = ['loyalty_points', 'is_verified']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        profile = instance.profile

        # User ma'lumotlarini yangilash
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.save()

        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    phone_number = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'phone_number']

    def validate_phone_number(self, value):
        if UserProfile.objects.filter(phone_number=value).exists():
            raise serializers.ValidationError("Bu telefon raqami allaqachon ro'yxatdan o'tgan.")
        return value

    def create(self, validated_data):
        phone_number = validated_data.pop('phone_number')
        password = validated_data.pop('password')

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        user.profile.phone_number = phone_number
        user.profile.save()

        return user


