from django.test import Client
import pytest
from http import HTTPStatus
from madr.routers.contas.models import User
from madr.routers.auths.schemas import TokenSchema

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


@pytest.mark.django_db
def test_create_token_invalid(client: Client, other_user: User):
    response = client.post(
        '/api/v1/auth/token',
        data = {
            'username': other_user.username,
            'password': "",
        },
        content_type='application/json'
    )

    response_json = response.json() 

    assert response_json['message'] == "Credenciais inválidas"
    assert response.status_code == HTTPStatus.UNAUTHORIZED


