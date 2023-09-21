from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from users.serializers import UserRegisterCashedModelSerializer, UserRetrieveUpdateDestroyModelSerializer, \
    CheckActivationCode


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
        return Response(serializer.data, status=status.HTTP_200_OK)
