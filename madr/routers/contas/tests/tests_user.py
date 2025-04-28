from madr.routers.contas.factories import UserFactory
import pytest
import json
from madr.routers.contas.models import User
from http import HTTPStatus

@pytest.mark.django_db(transaction=True, reset_sequences=True)
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
def test_create_test_error_conflict(client, user):
    username = 'thiago'
    other_user = UserFactory(username=username)


    response = client.post(
        "/api/v1/contas/",
        data={
            'username': user.username,
            'email': 'qualquercoisa@gmail.com',
            'password': '123'
        },
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json().get('message') == 'Email ou Username já consta no banco'




@pytest.mark.django_db
def test_update_user(user, client, token):
    response = client.put(
        f"/api/v1/contas/{user.id}",
        headers={'Authorization': f'Bearer {token}'},
        data = {
            'username': 'bob',
            'email': 'lmpcddp@nada.com',
            'password': '1234',
        },
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'bob',
        'email': 'lmpcddp@nada.com',
        'id': user.id,
    }

@pytest.mark.django_db
def test_user_update_not_authorize(client, token, user):
    response = client.put(
        f'/api/v1/contas/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        data={
            'username': 'outro',
            'email': 'soadjdosa@odasodsa.com',
            'password': '123'
        },
        content_type="application/json"
    )
    __import__('ipdb').set_trace()

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {'message': 'Não autorizado'}

@pytest.mark.django_db
def test_user_not_found(client, user, token):
    response = client.put(
        f'/api/v1/contas/{-user.id}',
        headers={'Authorization': f'Bearer {token}'},
        data={
            'username': 'outro',
            'email': 'soadjdosa@odasodsa.com',
            'password': '123',
        },
        content_type="application/json"
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'message': 'Usuário não encontrado'}