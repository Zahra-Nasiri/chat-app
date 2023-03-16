from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str
    is_admin: bool

class LoginUser(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    uid: str
    token: str