from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from .models import User, LoginUser
from .db import Datebase
from fastapi import Header

router = InferringRouter()

db_client = Datebase()

@cbv(router)
class UserRouter:

    @router.post("/register")
    async def register(self, user: User):
        return await db_client.create_user(user)

    @router.post("/login")
    async def login(self, user:LoginUser):
        return await db_client.authenticate_user(user)

