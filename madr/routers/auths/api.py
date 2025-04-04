from http import HTTPStatus
from ninja import Router
from .schemas import AuthBearer, TokenSchema, Message, LoginSchema
from django.contrib.auth.hashers import make_password, check_password
from jwt import decode, encode
from django.conf import settings
from madr.routers.contas.models import User
from datetime import datetime, timedelta

router = Router(tags=['auth'])


auth_bearer = AuthBearer()


@router.post("/token", response={HTTPStatus.OK: TokenSchema, HTTPStatus.UNAUTHORIZED: Message})
def login(request, data: LoginSchema):

    user = User.objects.filter(username=data.username).first()

    if user and check_password(data.password, user.password):
        access_token = encode(
            {"sub": user.username, "id": user.id, "exp": datetime.utcnow() + timedelta(minutes=60)},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return HTTPStatus.OK, {"access_token": access_token, "token_type": "bearer"}

    return HTTPStatus.UNAUTHORIZED, {"message": "Credenciais inválidas"}
