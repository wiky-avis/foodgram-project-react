import pytest


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='AdminUser', email='admin@foodgram.fake', password='1234567'
    )


@pytest.fixture
def token(admin):
    from rest_framework.authtoken.models import Token

    token, errors = Token.objects.get_or_create(user=admin)

    return {
        'auth_token': str(token)
    }


@pytest.fixture
def admin_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Authorization: Token {token["auth_token"]}')
    return client


@pytest.fixture
def auth_user(django_user_model):
    return django_user_model.objects.create_user(
        username='TestUser', email='test_user@foodgram.fake', password='1234567'
    )


@pytest.fixture
def token(auth_user):
    from rest_framework.authtoken.models import Token

    token, errors = Token.objects.get_or_create(user=auth_user)

    return {
        'auth_token': str(token)
    }


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Authorization: Token {token["auth_token"]}')
    return client
