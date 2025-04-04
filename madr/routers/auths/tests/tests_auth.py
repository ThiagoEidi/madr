from madr.routers.contas.factories import UserFactory
import pytest
from django.contrib.auth.hashers import make_password
import json
from http import HTTPStatus

@pytest.mark.django_db
def test_user_update_not_authorize(client):
    password='123'
    user = UserFactory(password=make_password(password))
    username = 'qualquerloucura'
    other_user = UserFactory(username=username, password=password)

    response = client.post(
        '/api/v1/auth/token',
        data={'username': user.username, 'password': password},
        content_type="application/json"
    )
    token = response.json()['access_token']

    response = client.put(
        f'/api/v1/contas/{other_user.id}',
        headers={'Authorization': f'Bearer {token}'},
        data={
            'username': 'outro',
            'email': 'soadjdosa@odasodsa.com',
            'password': '123'
        },
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'message': 'Não autorizado'}