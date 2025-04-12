from ninja import Schema
from ninja.orm import ModelSchema
from pydantic import EmailStr

from .models import User

class Message(Schema):
    message: str

class UserSchema(ModelSchema):
    email: EmailStr

    class Meta:
        model = User
        fields = ['username', 'password']

# class UserSchema(Schema):
#     email: str
#     username: str
#     password: str

class UserPublic(ModelSchema):
    email: EmailStr

    class Meta:
        model = User
        fields = ['username', 'id']


