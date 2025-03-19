from ninja import Router
from .models import User
from .schemas import UserSchema, UserPublic
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password

router = Router(tags=['contas'])

@router.post("/users/", response=UserPublic)
def create_user(request, user: UserSchema):
    if User.objects.filter(email=user.email).exists():
        return HttpResponse("Email already registered.", status=400)
    if User.objects.filter(username=user.username).exists():
        return  HttpResponse("Username already registered.", status=400)

    hashed_password = make_password(user.password)
    new_user = User.objects.create(
        username=user.username,
        email=user.email,
        password=hashed_password
    )
    return new_user

