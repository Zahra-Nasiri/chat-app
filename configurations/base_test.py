from settings import get_settings
from pymongo import MongoClient


settings = get_settings()


class TestConfiguration:
    db_client = MongoClient(settings.MONGO_DB_URL)
    user_collection = db_client[settings.DB][settings.user_collection]
    token_collection = db_client[settings.DB][settings.token_collection]