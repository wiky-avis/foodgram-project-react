import pytest

from .common import auth_client, create_tags


class TestApiTags:

    @pytest.mark.django_db(transaction=True)
    def test_list_tags(self, client):
        response = client.get('/api/tags/')
        assert response.status_code == 200

        data = response.json()

        data_2 = [
            {
                "id": 1,
                "name": "Борщ",
                "color": "#ffffff",
                "slug": "borsh"
                },
            {
                "id": 2,
                "name": "Суп",
                "color": "#ff00ff",
                "slug": "sup"
                }
            ]

        assert data == data_2
