from ninja import Schema
from ninja.orm import ModelSchema
from .models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UserPublic(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'email', 'id']


