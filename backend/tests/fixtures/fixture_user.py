import pytest


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_superuser(
        username='TestUser', email='admin@foodgram.fake', password='1234567'
    )


@pytest.fixture
def token(admin):
    from rest_framework.authtoken.models import Token

    token = Token.objects.get_or_create(user=admin)

    return {
        'auth_token': str(token.key)
    }


@pytest.fixture
def user_client(token):
    from rest_framework.test import APIClient

    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Authorization: Token {token["auth_token"]}')
    return client
