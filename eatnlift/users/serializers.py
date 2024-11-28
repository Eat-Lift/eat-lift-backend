from rest_framework import serializers
from django.contrib.auth.models import User
from .models import CustomUser, UserProfile, Check

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'description', 'picture']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['birth_date', 'genre', 'height', 'weight', 'goal', 'activity', 'calories', 'proteins', 'fats', 'carbohydrates']

class CheckSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Check
        fields = ['user_id', 'date', 'weight', 'bodyfat', 'neck', 'shoulders', 'arm', 'chest', 'waist', 'hip', 'thigh', 'calf']