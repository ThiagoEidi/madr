from http import HTTPStatus
from ninja import Router
from django.db.models import Q
from .models import User
from .schemas import UserSchema, UserPublic, Message
from django.contrib.auth.hashers import make_password
from madr.routers.auths.api import auth_bearer



router = Router(tags=['contas'])


@router.post("/", response={HTTPStatus.CREATED: UserPublic, HTTPStatus.CONFLICT: Message})
def create_user(request, user: UserSchema):
    if User.objects.filter(Q(email=user.email) | Q(username=user.username)).exists():
        return HTTPStatus.CONFLICT, {'message': 'Email ou Username já consta no banco'}

    hashed_password = make_password(user.password)
    new_user = User.objects.create(
        username=user.username,
        email=user.email,
        password=hashed_password
    )

    return HTTPStatus.CREATED, new_user


errors = frozenset({HTTPStatus.CONFLICT, HTTPStatus.NOT_FOUND, HTTPStatus.FORBIDDEN})
@router.put(
    "/{user_id}",
    response={HTTPStatus.OK: UserPublic, errors: Message},
    auth=auth_bearer
)
def update_user(request, user: UserSchema, user_id: int):
    if int(request.auth["id"]) != int(user_id):
        return HTTPStatus.FORBIDDEN, {'message': "Não autorizado"}

    try:
        existing_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HTTPStatus.NOT_FOUND, {"message": "Usuário não encontrado"}

    if User.objects.filter(Q(email=user.email) | Q(username=user.username)).exclude(id=user_id).exists():
        return HTTPStatus.CONFLICT, {'message': 'Email ou Username já consta no banco'}

    existing_user.username = user.username
    existing_user.email = user.email

    if user.password:
        existing_user.password = make_password(user.password)

    existing_user.save()

    return existing_user

