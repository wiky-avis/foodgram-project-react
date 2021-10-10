from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from recipes.models import Tag


def auth_client(user):
    token = Token.objects.get_or_create(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Authorization: Token {token.key}')
    return client


def create_tags(user_client):
    tag = Tag.objects.create(name='Борщ', color='#ffffff', slug='borsh')
    data1 = {
        'name': {tag.name},
        'color': {tag.color},
        'slug': {tag.slug}
    }

    tag_2 = Tag.objects.create(name='Суп', color='#ff00ff', slug='sup')
    data2 = {
        'name': {tag_2.name},
        'color': {tag_2.color},
        'slug': {tag_2.slug}
    }
    return [data1, data2]
