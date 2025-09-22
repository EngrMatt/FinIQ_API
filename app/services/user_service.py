from typing import Optional
from app.schemas.user_schema import UserCreate, UserResponse
from app.core.settings import settings, logger

# 模擬資料庫 (之後可換成真正的 DB)
fake_db = {}

class UserService:
    def create_user(self, user: UserCreate) -> UserResponse:
        # logger.info("Fetching users from database: %s", settings.database_url)
        new_id = len(fake_db) + 1
        user_data = UserResponse(id=new_id, name=user.name, email=user.email)
        fake_db[new_id] = user_data
        return user_data

    def get_user(self, user_id: int) -> Optional[UserResponse]:
        return fake_db.get(user_id)
