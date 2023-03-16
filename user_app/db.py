import configurations.base_db as base_db
from configurations.base_db import (
    DatabaseConfiguration,
    start_db
)
from .models import User, LoginUser, Token
import bcrypt
from bson.objectid import ObjectId
import jwt

class Datebase(DatabaseConfiguration):
    secret_key = "A26744858F3E9DDED3E329F5FA76A"
    async def hash_password(self, password: str):
        salt = b'$2b$12$BP41xhckoXNw9/fhotVpH.'
        return bcrypt.hashpw(password.encode() , salt)

    @start_db()
    async def get_user(self, user_id):
        query = await base_db.client.user_collection.find_one({"_id": user_id})
        query["_id"] = str(query["_id"])
        query.pop('password')
        return query


    @start_db()
    async def create_user(self, user: User):
        user.password = await self.hash_password(user.password)
        query = await base_db.client.user_collection.insert_one(user.dict())
        result = await self.get_user(query.inserted_id)
        return result

    @start_db()
    async def create_token(self, uid: str):
        token = jwt.encode({"uid": uid}, self.secret_key, algorithm="HS256")
        token_object = Token(uid=uid, token=token)
        await base_db.client.token_collection.insert_one(token_object.dict())
        return token_object.dict()

    @start_db()
    async def authenticate_user(self, user: LoginUser):
        query = await base_db.client.user_collection.find_one({"username": user.username})
        if (not query) or (query["password"] != await self.hash_password(user.password)):
            return None

        return await self.create_token(str(query["_id"]))

