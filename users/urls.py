from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView

from users.views import (
    RegisterUserCreateAPIView, ActivationUserGenericAPIView, PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView, UserRetrieveAPIView)

app_name = 'users'

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('register', RegisterUserCreateAPIView.as_view(), name='register'),
    path('activate', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('forget-password', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),
    path('me', UserRetrieveAPIView.as_view(), name='me')
]
