from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import UserRegisterCashedCreateAPIView, UserRetrieveAPIView, CheckActivationCodeGenericAPIView

urlpatterns = [
    path('register', UserRegisterCashedCreateAPIView.as_view(), name='register'),
    path('me', UserRetrieveAPIView.as_view(), name='me'),
    path('activate-code', CheckActivationCodeGenericAPIView.as_view(), name='activate-code'),
    path('login', TokenObtainPairView.as_view(), name='token'),
]
