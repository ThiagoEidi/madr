from http import HTTPStatus
from ninja import Router
from django.db.models import Q
from .models import User
from .schemas import UserSchema, UserPublic, Message
from django.contrib.auth.hashers import make_password
from ninja.security import HttpBearer
from django.contrib.auth import authenticate
import datetime
from ninja import Schema
import jwt

from ...settings import SECRET_KEY


class LoginSchema(Schema):
    username: str
    password: str

class JWTBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        if user_id := payload.get("sub"):
            return User.objects.get(id=user_id)

        return None

router = Router(tags=['contas'])

SECRET_KEY = 'QUALQUERCOISA'
ALGORITHM = 'HS256'

@router.post("/login")
def create_token(request, credencials: LoginSchema):
    user = authenticate(username=credencials.username, password=credencials.password)
    if user is not None:
        # Usuário autenticado com sucesso
        # Cria o payload com os claims do JWT
        payload = {
            "sub": str(user.id),  # ID do usuário
            "username": user.username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)  # Expiração em 30 min
        }

        # Gera o token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": token, "token_type": "bearer"}
    else:
        # Retorna erro de autenticação
        return {"error": "Credenciais inválidas"}, 401

@router.post("/users/", response={HTTPStatus.CREATED: UserPublic, HTTPStatus.CONFLICT: Message})
def create_user(request, user: UserSchema):
    if User.objects.filter(Q(email=user.email) | Q(username=user.username)).exists():
        return HTTPStatus.CONFLICT, {'message': 'Email ou Username ja consta no madr'}

    hashed_password = make_password(user.password)
    new_user = User.objects.create(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    return HTTPStatus.CREATED, new_user

@router.put("/users/{user_id}", response={HTTPStatus.OK: UserPublic, HTTPStatus.CONFLICT: Message}, auth=JWTBearer())
def upgrade_user(request, user: UserSchema):
    request.user



