from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from rest_framework.parsers import MultiPartParser, FormParser

User = get_user_model()  # This ensures you're using your custom user model

def get_auth_for_user(user):
    """
    Generate a JWT token for the user and return user data with token.
    """
    refresh = RefreshToken.for_user(user)
    return {
        'user': UserSerializer(user).data,
        'token': {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    }

class SignUpView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response_data = get_auth_for_user(user)
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignInView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response_data = get_auth_for_user(user)
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TestView(APIView):
    def get(self, request, format=None):
        return Response("You made it", status=200)
