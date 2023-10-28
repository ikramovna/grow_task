from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import UserRegisterCashedModelSerializer, UserRetrieveUpdateDestroyModelSerializer, \
    CheckActivationCode, SendEmailResetSerializer, PasswordResetConfirmSerializer
from users.services.cache_functions import getKey


# Create your views here.


class UserRegisterCashedCreateAPIView(CreateAPIView):
    serializer_class = UserRegisterCashedModelSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveUpdateDestroyModelSerializer
    # parser_classes = [FormParser, MultiPartParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class CheckActivationCodeGenericAPIView(GenericAPIView):
    serializer_class = CheckActivationCode

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        user = getKey(key=data['email'])['user']
        user.save()
        token = RefreshToken.for_user(user)
        response = {
            "access": str(token.access_token),
            'refresh': str(token),
        }
        return Response(response, status=status.HTTP_200_OK)



class PasswordResetGenericAPIView(GenericAPIView):
    serializer_class = SendEmailResetSerializer
    # parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        return Response({'email': email}, status=status.HTTP_200_OK)


class PasswordResetConfirmUpdateAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    # parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('new_password')
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)
