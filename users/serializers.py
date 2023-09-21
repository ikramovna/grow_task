import random

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail

from rest_framework import serializers

from root.settings import EMAIL_HOST_USER
from users.models import User
from users.services.cache_functions import setKey, getKey, deleteKey

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from users.services.validations_errors import Messages
from users.services.email import ActivationEmail

error_messages = Messages()

class UserRegisterModelSerializer(serializers.ModelSerializer):
    fullname = serializers.CharField(max_length=150, write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(max_length=150, write_only=True)
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "username", "password")


class UserRegisterCashedModelSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=150, write_only=True)

    class Meta:
        model = User
        fields = ("fullname", "email", "username", "password")

    def validate(self, attrs):
        activate_code = random.randint(100000, 999999)
        setKey(
            key=attrs['email'],
            value={
                "fullname": attrs['fullname'],
                "email": attrs['email'],
                "username": attrs['username'],
                "password": attrs['password'],
                "activate_code": activate_code
            },
            timeout=None
        )
        print(getKey(key=attrs['email']))
        send_mail(
            subject="Subject here",
            message=f"Your activate code.\n{activate_code}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[attrs['email']],
            fail_silently=False,
        )
        return super().validate(attrs)


class UserRetrieveUpdateDestroyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'id',
            'last_login',
            'is_superuser',
            'is_staff',
            'created_at',
            'updated_at',
            'groups',
            'user_permissions',
            'password',
            'first_name',
            'last_name'
        )


class CheckActivationCode(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    activate_code = serializers.IntegerField(write_only=True)

    def validate(self, attrs):
        data = getKey(key=attrs['email'])
        print(data)
        if data and data['activate_code'] == attrs['activate_code']:
            user = User.objects.create(
                fullname=data['fullname'],
                email=data['email'],
                username=data['username'],
                password=make_password(data['password']),
                is_active=True,
            )
            user.save()
            deleteKey(key=attrs['email'])
            return attrs
        raise serializers.ValidationError(
            {"error": "Error activate code or email"}
        )


class PasswordResetConfirmSerializer(serializers.Serializer):
    activation_code = serializers.IntegerField(write_only=True)
    email = serializers.EmailField(write_only=True)
    new_password = serializers.CharField(max_length=150, write_only=True)
    # confirm_password = serializers.CharField(max_length=150, write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs.get('email'))
            validate_password(attrs.get('new_password'), user)
            validate_password(attrs.get('confirm_password'), user)
        except (User.DoesNotExist, ValidationError) as e:
            raise serializers.ValidationError({"password": str(e)})

        return super().validate(attrs)


class SendEmailResetSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if not User.objects.filter(email=attrs.get('email')).exists():
            raise serializers.ValidationError({"email": error_messages.EMAIL_NOT_FOUND})
        user = User.objects.get(email=attrs.get('email'))
        self.context['user'] = user
        ActivationEmail(self.context.get('request'), self.context).send([user.email])
        return attrs
