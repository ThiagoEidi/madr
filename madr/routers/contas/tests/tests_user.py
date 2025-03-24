from http.client import responses
from os import access
import uuid

from madr.routers.contas.factories import UserFactory
import pytest
import json
from http import HTTPStatus

@pytest.mark.django_db
def test_create_user(client):
    response = client.post(
        "/api/v1/contas/",
        data=json.dumps({
            "username": "thiagoaaa",
            'email': 'thiagaaaao@email.com',
            "password": "123"
        }),
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'thiagoaaa',
        'email': 'thiagaaaao@email.com',
        'id': 1,
    }

@pytest.mark.django_db
def test_create_test_error_conflict(client):
    username = 'thiago'
    other_user = UserFactory(username=username)

    response = client.post(
        "/api/v1/contas/",
        data=json.dumps({
            'username': 'thiago',
            'email': 'qualquercoisa@gmail.com',
            'password': '123'
        }),
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json().get('message') == 'Email ou Username já consta no banco'


@pytest.mark.django_db
def test_user_update_not_authorize(client):
    username1 = f'user1_{uuid.uuid4()}'
    password = '123'
    user = UserFactory(username=username1, password=password)

    username2 = f'user2_{uuid.uuid4()}'
    other_user = UserFactory(username=username2)

    response = client.post(
        '/api/v1/contas/token',
        data={'username': user.username, 'password': '123'},
    )
    token = response.json()['access_token']

    response = client.put(
        f'/api/v1/contas/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        data=json.dumps({
            'username': 'outro',
            'email': 'soadjdosa@odasodsa.com',
            'password': '123'
        }),
        content_type = "application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'message': 'Não autorizado'}