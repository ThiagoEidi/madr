from ninja import Schema
from django.conf import settings
from ninja.security import HttpBearer
from jwt import decode

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM

class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        if payload:
            return payload
        
class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    token_type: str

class Message(Schema):
    message: str
