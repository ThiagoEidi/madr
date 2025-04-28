from ninja import Schema

class InvalidToken(Exception):
    pass

class LoginSchema(Schema):
    username: str
    password: str

class TokenSchema(Schema):
    access_token: str
    token_type: str

class Message(Schema):
    message: str
