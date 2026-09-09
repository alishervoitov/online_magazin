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


