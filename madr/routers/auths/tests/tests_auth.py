from madr.routers.contas.factories import UserFactory
import pytest
from django.contrib.auth.hashers import make_password
from http import HTTPStatus
from madr.routers.contas.models import User

@pytest.mark.django_db
def test_create_token(client, user: User):
    response = client.post(
        '/api/v1/auth/token',
        data = {
            'username': user.username,
            'password': user.clean_password,
        },
        content_type='application/json'
    )
    token = response.json()

    assert 'access_token' in token
    assert 'token_type' in token
    assert token['token_type'] == 'bearer'

