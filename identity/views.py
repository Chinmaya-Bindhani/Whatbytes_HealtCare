from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterUserSerializer, LoginSerializer, ViewMe

User = get_user_model()

def get_token(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token)
    }


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data['email'],
            password=serializer.validated_data['password'],
        )
        if not user:
            return Response({"detail": "Invalid email or password"}, status=401)

        return Response({"user": ViewMe(user).data, "token": get_token(user)})


class MeView(generics.RetrieveAPIView):
    serializer_class = ViewMe
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

