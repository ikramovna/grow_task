from django.urls import path

from users.views import (
    RegisterUserCreateAPIView,
    ActivationUserGenericAPIView,
    PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView,
    UserRetrieveAPIView
)

urlpatterns = [
    path('ragister/', RegisterUserCreateAPIView.as_view(), name='register'),
    path('activate/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),
    path('me/', UserRetrieveAPIView.as_view(), name='me')
]
