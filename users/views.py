from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView

from users.models import User
from users.serializers import PasswordResetConfirmSerializer
from users.serializers import (
    RegisterUserModelSerializer,
    CheckActivationSerializer,
    SendEmailResetSerializer,
    UserListModelSerializer,
    UserRetrieveSerializer
)


class RegisterUserCreateAPIView(CreateAPIView):
    serializer_class = RegisterUserModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)


class ActivationUserGenericAPIView(GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CheckActivationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetGenericAPIView(GenericAPIView):
    serializer_class = SendEmailResetSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        return Response({'email': email}, status=status.HTTP_200_OK)


class PasswordResetConfirmUpdateAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('new_password')
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)


class UserGenericAPIView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserListModelSerializer

    def get(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
