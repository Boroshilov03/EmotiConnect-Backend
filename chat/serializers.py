from rest_framework import serializers
from .models import User
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, 
        max_length=32, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        required=True, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    first_name = serializers.CharField(
        required=True, 
        max_length=32
    )
    last_name = serializers.CharField(
        max_length=32
    )
    phone_number = serializers.CharField(
        required=True, 
        max_length=15, 
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True, 
        min_length=8, 
        write_only=True
    )

    def create(self, validated_data):
        password = validated_data.pop('password')  # Extract the password
        user = self.Meta.model(**validated_data)  # Create a user instance
        user.set_password(password)  # Hash the password
        user.save()  # Save the user instance
        return user

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'phone_number', 'thumbnail', 'password']

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        user = authenticate(username=username, password=password)  # Authenticate user
        if not user:
            raise serializers.ValidationError("Invalid username or password")
        return {'user': user}

    def get_token(self, obj):
        """
        Generate a JWT token for the user instance.
        """
        user = obj['user']
        refresh = RefreshToken.for_user(user)  # Create a refresh token for the user
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
