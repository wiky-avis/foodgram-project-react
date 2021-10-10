from http import HTTPStatus

import pytest

from .common import create_users
from django.contrib.auth import get_user_model


class TestApiUser:

    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        'email, username, first_name, last_name, password, status_code', [
            (None, None, None, None, None, HTTPStatus.BAD_REQUEST),
            ('test1@test.ru', None, None, None, 'user_pass', HTTPStatus.BAD_REQUEST),
            ('test2@test.ru', 'user_test', 'Anna', None, 'user_pass', HTTPStatus.BAD_REQUEST),
            ('test3@test.ru', 'user_test2', 'Vasya', 'Pupkin', 'user_pass', HTTPStatus.CREATED)
        ])
    def test_registration_user(
            self, api_client, email, username, first_name, last_name, password, status_code
    ):
        data = {
            'email': email,
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }
        response = api_client.post('/api/users/', data=data, format='json')
        assert response.status_code == status_code

    @pytest.mark.django_db(transaction=True)
    def test_get_list_users(self, api_client, django_user_model):
        create_users(django_user_model)

        response = api_client.get('/api/users/')
        assert response.status_code == HTTPStatus.OK
        data = response.json()

        expected = {
            'count': 2,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': 2,
                    'email': 'vgaksentii@test.ru',
                    'username': 'vg',
                    'first_name': 'Victoria',
                    'last_name': 'Axentii'
                },
                {
                    'id': 1,
                    'email': 'vpupkin@yandex.ru',
                    'username': 'vasya.pupkin',
                    'first_name': 'Вася',
                    'last_name': 'Пупкин'
                }
            ]
        }
        assert data == expected


    @pytest.mark.django_db(transaction=True)
    @pytest.mark.parametrize(
        "data, http_status", [
            ({'email': 'test_user@foodgram.fake', 'password': '1234567'}, HTTPStatus.CREATED),
            ({'email': None, 'password': None}, HTTPStatus.UNAUTHORIZED)
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
