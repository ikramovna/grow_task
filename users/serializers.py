from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions

from rest_framework.settings import api_settings
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.services.cache_function import getKey, deleteKey
from users.services.email import ActivationEmail

User = get_user_model()


class RegisterUserModelSerializer(ModelSerializer):
    password = serializers.CharField(max_length=100, write_only=True)

    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + ('fullname', 'email', 'password')

    # def check_password_macht(self, **kwargs):
    #     if kwargs.get("password") != kwargs.get("re_password"):
    #         raise serializers.ValidationError({"password_mismatch": 'error_messages.PASSWORD_MISMATCH_ERROR'})
    #     return True
    #
    # def validate(self, attrs):
    #     if self.check_password_macht(**attrs):
    #         attrs.pop('re_password')
    #         try:
    #             user = User(**attrs)
    #             validate_password(attrs.get('password'), user)
    #         except django_exceptions.ValidationError as e:
    #             serializer_error = serializers.as_serializer_error(e)
    #             raise serializers.ValidationError(
    #                 {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
    #             )
    #     return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        self.context['user'] = user
        ActivationEmail(self.context.get('request'), self.context).send([user.email])
        return user


class CheckActivationSerializer(serializers.Serializer):
    activation_code = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        if getKey(attrs.get('email')) != attrs.get('activation_code'):
            raise serializers.ValidationError({"invalid_code": 'error_messages.INVALID_ACTIVATE_CODE_ERROR'})
        deleteKey(attrs.get('email'))
        return attrs


class PasswordResetConfirmSerializer(CheckActivationSerializer):
    new_password = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get('email'))
            validate_password(attrs.get('new_password'), user)
        except django_exceptions.ValidationError as e:
            serializer_error = serializers.as_serializer_error(e)
            raise serializers.ValidationError(
                {"password": serializer_error[api_settings.NON_FIELD_ERRORS_KEY]}
            )

        return super().validate(attrs)


class SendEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": 'error_messages.EMAIL_NOT_FOUND'})
        user = User.objects.get(email=attrs.get('email'))
        self.context['user'] = user
        ActivationEmail(self.context.get('request'), self.context).send([user.email])
        return attrs


class UserListModelSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'fullname',  'is_active', 'created_at')


class UserRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'email', 'fullname',
            'is_active', 'created_at'
        )


class UserRegisterCashSerializer(serializers.Serializer):
    full_name = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=150)