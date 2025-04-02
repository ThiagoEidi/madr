from madr.routers.contas.factories import UserFactory
import pytest
from django.contrib.auth.hashers import make_password
import json
from http import HTTPStatus

@pytest.mark.django_db()
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

@pytest.mark.django_db()
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


@pytest.mark.django_db()
def test_user_update_not_authorize(client):
    password='123'
    user = UserFactory(password=make_password(password))
    user.save()
    username = 'qualquerloucura'
    other_user = UserFactory(username=username, password=password)
    other_user.save()

    print(user.password)

    response = client.post(
        '/api/v1/contas/token',
        data=json.dumps({'username': user.username, 'password': password}),
        content_type="application/json"
    )
    print(f'Resposta {response.json()}')
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