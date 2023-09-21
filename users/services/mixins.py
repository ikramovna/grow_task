from rest_framework import status
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.generics import GenericAPIView
from rest_framework.generics import GenericAPIView

class SendEmailActivationCodeMixin:
    def send_email(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        response_data = {'success': email}
        headers = self.get_success_headers(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        location = data.get(api_settings.URL_FIELD_NAME)
        if location:
            return {'Location': str(location)}
        return {}

class SendEmailActivationCodeView(SendEmailActivationCodeMixin, GenericAPIView):
    def post(self, request, *args, **kwargs):
        return self.send_email(request)





class CheckActivationCodeMixin:
    def check_activation_code(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        response_data = {'message': 'success'}
        headers = self.get_success_headers(serializer.data)

        return Response(response_data, status=status.HTTP_200_OK, headers=headers)

    def get_success_headers(self, data):
        location = data.get(api_settings.URL_FIELD_NAME)
        if location:
            return {'Location': str(location)}
        return {}


class CheckActivationCodeView(CheckActivationCodeMixin, GenericAPIView):
    def post(self, request):
        return self.check_activation_code(request)

