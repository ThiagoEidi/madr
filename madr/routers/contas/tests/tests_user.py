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
