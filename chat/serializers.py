from rest_framework import serializers
from .models import User  # Make sure to import your custom user model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'thumbnail']
