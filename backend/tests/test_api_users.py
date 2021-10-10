from http import HTTPStatus

import pytest
from rest_framework.test import APIClient


class TestApiUser:

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "data, http_status", [
            ({'email': 'test_user@foodgram.fake', 'password': '1234567'}, HTTPStatus.CREATED),
            ({'email': '', 'password': ''}, HTTPStatus.UNAUTHORIZED)
        ]
    )
    def test_users_get_token(self, user_client, data, http_status):
        data = data
        response = user_client.post('/api/auth/token/login/', data=data)
        assert response.status_code == http_status

    @pytest.mark.django_db(transaction=True)
    def test_admin_get_token(self, admin_client, admin):
        data = {
            'email': 'admin@foodgram.fake',
            'password': '1234567'
        }
        response = admin_client.post('/api/auth/token/login/', data=data)
        assert response.status_code == HTTPStatus.CREATED

    @pytest.mark.django_db(transaction=True)
    def test_registration_user_and_get_token(self):
        client = APIClient()
        data = {
            "email": "vpupkin@yandex.ru",
            "username": "vasya_pupkin",
            "first_name": "Вася",
            "last_name": "Пупкин",
            "password": "Qwerty123"
        }
        response = client.post('/api/users/', data=data, format='json')
        assert response.status_code == HTTPStatus.CREATED
