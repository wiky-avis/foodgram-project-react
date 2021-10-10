from http import HTTPStatus

import pytest

from .common import auth_client, create_tags


class TestApiTags:

    @pytest.mark.django_db(transaction=True)
    def test_get_list_tags(self, user_client, admin):
        create_tags(user_client)

        response = user_client.get('/api/tags/')
        assert response.status_code == HTTPStatus.OK
        data = response.json()

        expected = [
            {
                'id': 1,
                'name': 'Борщ',
                'color': '#ffffff',
                'slug': 'borsh'
                },
            {
                'id': 2,
                'name': 'Суп',
                'color': '#ff00ff',
                'slug': 'sup'
                }
            ]
        assert data == expected
