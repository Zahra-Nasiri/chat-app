from configurations.base_test import TestConfiguration
from bson.objectid import ObjectId
import bcrypt
import jwt
from user_app.models import Token

class TestSetup(TestConfiguration):

    secret_key = "A26744858F3E9DDED3E329F5FA76A"

    def hash_password(password: str):
        salt = b'$2b$12$BP41xhckoXNw9/fhotVpH.'
        return bcrypt.hashpw(password.encode() , salt)

    fake_user = {
        "username": "test user",
        "password": "a123gsdga3423",
        "first_name": "test first_name",
        "last_name": "test last_name",
        "is_admin": False
    }

    fake_user_update = {
        "first_name": "updated first_name",
        "last_name": "updated last_name"
    }

    fake_user_login = {
        "username": "myuserloginname",
        "password": "a123gsdga3423"
    }

    fake_user_create = {
        "username": "myuserloginname",
        "password": hash_password("a123gsdga3423"),
        "first_name": "test first_name",
        "last_name": "test last_name"
    }

    def create_fake_user(self):
        return self.user_collection.insert_one(self.fake_user)

    def get_user(self, user_id):
        return self.user_collection.find_one({"_id": ObjectId(user_id)})

    def create_fake_user_login(self):
        return self.user_collection.insert_one(self.fake_user_create)

    def create_fake_user_login_for_token(self):
        user = {
            "first_name": "test value",
            "last_name": "test value",
            "username": "test_value",
            "password": "2425lkjlkl",
            "is_admin": False
        }
        return self.user_collection.insert_one(user)

    def create_token(self, uid):
        token = jwt.encode({"uid": uid}, self.secret_key, algorithm="HS256")
        token_object = Token(uid=uid, token=token)
        return self.token_collection.insert_one(token_object.dict())

    def get_token(self, token_id):
        return self.token_collection.find_one({"_id": ObjectId(token_id)})