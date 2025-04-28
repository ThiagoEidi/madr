from http import HTTPStatus
from ninja import Router
from .schemas import TokenSchema, Message, LoginSchema, InvalidToken
from django.contrib.auth.hashers import make_password, check_password
from jwt import decode, encode
from django.conf import settings
from madr.routers.contas.models import User
from datetime import datetime, timedelta
from ninja.security import HttpBearer
from jwt import decode
from jwt.exceptions import DecodeError



router = Router(tags=['auth'])


SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class AuthBearer(HttpBearer):
    def authenticate(self, request, token, user_id=None):
        try:
            __import__('ipdb').set_trace()
            decode_token = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except DecodeError:
            return router.api.create_response(request, {"detail": "Invalid token supplied"}, status=401)
        

auth_bearer = AuthBearer()




@router.post("/token", response={HTTPStatus.OK: TokenSchema, HTTPStatus.UNAUTHORIZED: Message})
def login(request, data: LoginSchema):
    try: 
        user = User.objects.get(username=data.username)
        if not check_password(data.password, user.password):
            raise
        access_token = encode(
            {"sub": user.username, "id": user.id, "exp": datetime.now() + timedelta(minutes=60)},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )
        return HTTPStatus.OK, {"access_token": access_token, "token_type": "bearer"}
    
    except Exception:
        status_code = HTTPStatus.UNAUTHORIZED
        msg_error =  {"message": "Credenciais inválidas"}

    return status_code, msg_error