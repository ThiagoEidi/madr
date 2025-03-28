from http import HTTPStatus
from ninja import Router
from django.db.models import Q
from .models import User
from .schemas import UserSchema, UserPublic, Message
from django.contrib.auth.hashers import make_password, check_password
import datetime
from django.conf import settings
from ninja import Schema
from ninja.security import HttpBearer
from jwt import decode, encode
from datetime import datetime, timedelta

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload:
            return payload


auth_bearer = AuthBearer()


router = Router(tags=['contas'])

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    token_type: str


@router.post("/token", response={HTTPStatus.OK: TokenSchema, HTTPStatus.UNAUTHORIZED: Message})
def login(request, data: LoginSchema):

    user = User.objects.filter(username=data.username).first()

    if user and check_password(data.password, user.password):
        access_token = encode(
            {"sub": user.username, "id": user.id, "exp": datetime.utcnow() + timedelta(minutes=60)},
            SECRET_KEY,
            algorithm=ALGORITHM,
        )
        return HTTPStatus.OK, {"access_token": access_token, "token_type": "bearer"}

    return HTTPStatus.UNAUTHORIZED, {"message": "Credenciais inválidas"}

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

