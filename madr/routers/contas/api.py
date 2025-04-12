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
def update_user(request, user_id: int, user: UserSchema):
    try:
        user_db = User.objects.get(id=user_id)
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = make_password(user.password)
        user_db.save()
        return HTTPStatus.OK, user_db


    except User.DoesNotExist as e:
        status_code = HTTPStatus.NOT_FOUND
        error_msg = {"message": "Usuário não encontrado"}

    except Exception as e:
        status_code = HTTPStatus.BAD_REQUEST
        error_msg = {"message": str(e)}

    return status_code, error_msg


