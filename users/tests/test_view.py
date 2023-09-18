import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from users.services.cache_function import getKey


@pytest.mark.django_db
class TestActivationUserGenericAPIView:
    activate_code = ''
    client = APIClient()
    payload = dict(

        email="diordev@icloud.com",
        username="diordev",
        password="b2002234",
        re_password="b2002234",
    )

    urls = {
        'register': reverse('register'),
        'activate': reverse('activated_account'),
        'reset_password': reverse('reset_password'),
        'reset_password_confirm': reverse('reset_password_confirm')

    }

    @pytest.fixture
    def test_user_register(self):
        response = self.client.post(self.urls.get('register'), self.payload)

        data = response.data
        assert response.status_code == status.HTTP_201_CREATED
        assert "password" not in data
        assert data["email"] == self.payload["email"]

    def test_user_activation(self, test_user_register):
        data = {
            'email': self.payload.get('email'),
            'activation_code': getKey(self.payload.get('email'))
        }
        response = self.client.post(self.urls.get('activate'), data)
        assert response.status_code == status.HTTP_200_OK

    def test_user_activation_invalid_data(self):
        data = {'email': 'invalid-email'}
        response = self.client.post(self.urls.get('activate'), data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @pytest.fixture
    def test_user_reset_password(self, test_user_register):
        data = {
            'email': self.payload.get('email'),
        }
        response = self.client.post(self.urls.get("reset_password"), data)
        if response.status_code == status.HTTP_200_OK:
            assert response.status_code == status.HTTP_200_OK
        else:
            assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_reset_password_confirm(self, test_user_reset_password):
        data = {
            'email': self.payload.get('email'),
            'activation_code': getKey(self.payload.get('email')),
            'new_password': 'maryam0113',

        }

        response = self.client.patch(self.urls.get("reset_password_confirm"), data)
        assert response.status_code == status.HTTP_200_OK
