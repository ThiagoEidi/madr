from http import HTTPStatus
from ninja import Router

from .schemas import UserSchema

router = Router(tags=['contas'])

@router.post("/")
def create_username(request, payload: UserSchema):
    user = UserSchema.objects.create(**payload.dict())
    return {"username": user.username}